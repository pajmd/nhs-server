from flask import Flask, render_template, jsonify, request
from app.solr.solrclient import solr_search
from app.user import User, UserAlreadyExists, UserCreateError, UserFindError
from app.utils.helper import get_jwt, user_authorized
import os
from logging.config import dictConfig
from flask.logging import default_handler
import logging


class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s %(funcName)s - %(lineno)d: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

NHS_UI_DIST = os.getenv("NHS_UI_DIST", "../../../../js_workspace/VueProjects/nhs-ui/dist")
app = Flask("nhs-app",
            static_url_path='',
            static_folder=NHS_UI_DIST,
            template_folder=NHS_UI_DIST)


@app.route('/api/search', methods=['POST'])
def search():
    status_code = 200
    if request.method == 'POST':
        app.logger.info("Request: %s" % request.get_json())
        if user_authorized(request.headers):
            response = solr_search(request.get_json())
        else:
            status_code = 401
            response = {
                'authorized': False,
                'message': 'User not authorized'
            }

    else:
        app.logger.info('No idea what this request is')
        response = {
            'error': 'Search request not recognized'
        }
    return jsonify(response), status_code

# for error handling investigate: http://flask.pocoo.org/docs/1.0/patterns/apierrors/


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app.logger.info("Request: %s" % request.get_json())
        user_details = request.get_json()
        user = User(user_details)
        status_code = 200
        try:
            authenticated_user = user.authenticate_user()
            if authenticated_user:
                authenticated_user.update(
                    {
                        'authorized': True,
                        'token': get_jwt(authenticated_user)
                    }
                )
                response = authenticated_user
            else:
                status_code = 401
                response = {
                    'authorized': False,
                    'message': 'Wrong credentials'
                }
        except UserCreateError as e:
            status_code = 500
            response = {
                'authorized': False,
                'message': str(e),
            }
        except UserFindError as e:
            status_code = 500
            response = {
                'authorized': False,
                'message': str(e),
            }

    else:
        app.logger.info('No idea what this request is')
        status_code = 400
        response = {
            'authorized': False
        }
    return jsonify(response), status_code


@app.route('/api/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        app.logger.info("Request: %s" % request.get_json())
        user_details = request.get_json()
        user = User(user_details)
        status_code = 200
        try:
            new_user = user.create_user()
            response = {
                'authorized': True,
                'token': get_jwt(new_user),
                'email': new_user['email'],
                'first_name': new_user['first_name'],
                'last_name': new_user['last_name']
            }
        except UserAlreadyExists as e:
            status_code = 400
            response = {
                'authorized': False,
                'message': str(e)
            }
        except UserCreateError as e:
            status_code = 500
            response = {
                'authorized': False,
                'message': str(e)
            }
        except Exception as e:
            status_code = 500
            response = {
                'authorized': False,
                'message': str(e),
            }
    else:
        app.logger.info('No idea what this request is')
        status_code = 400
        response = {
            'authorized': False
        }
    return jsonify(response), status_code



# why do we need it? see Vue Router catch all route
# https://router.vuejs.org/guide/essentials/history-mode.html#example-server-configurations
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template("index.html")


@app.route('/')
def index():
    return render_template("index.html")


# begin just to test
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    # ex:
    # curl http://192.168.1.4:5000/user/toto  returns toto
    # curl http://192.168.1.4:5000/user/toto/ returns 404 whereas <username:path> would retuen toto/
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    # ex:
    # curl http://192.168.1.4:5000/post/123   returns 123
    # curl http://192.168.1.4:5000/post/abc  returns 404
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    # ex:
    # curl http://192.168.1.4:5000/path/toto  returns toto
    # curl http://192.168.1.4:5000/path/toto/  returns toto/
    # curl http://192.168.1.4:5000/path/toto/abc/def  returns toto/abc/def
    return 'Subpath %s' % subpath
# end just to test


# an alternative way to $ flask run --host=192.168.1.4 is app.run()
# but it is not recommended
if __name__ == "__main__":
    app.logger.info("Logger name: %s" % app.logger.name)
    app.debug = True  # NOT to use in PROD - allow the server to reload autonmatically after each change of code
    # app.run(host="192.168.1.4",)
    app.logger.info('NHS_UI_DIST: %s' % NHS_UI_DIST)
    cwd = os.getcwd()
    app.logger.info("cwd=%s" % cwd)
    ls = os.listdir(NHS_UI_DIST)
    app.logger.info('ls = %s' % ','.join(ls))
    app.run(host="0.0.0.0",)