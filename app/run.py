from flask import Flask, render_template, jsonify, request
from app.solr.solrclient import solr_search


app = Flask(__name__,
            static_url_path='',
            static_folder = "../../../../js_workspace/VueProjects/nhs-ui/dist",
            template_folder = "../../../../js_workspace/VueProjects/nhs-ui/dist")


@app.route('/api/search', methods=['POST'])
def search():
    if request.method == 'POST':
        print("Request: %s" % request.get_json())
        response = solr_search(request.get_json())
    else:
        print('No idea what this request is')
        response = {
            'error': 'Search request not recognized'
        }
    return jsonify(response)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Request: %s" % request.get_json())
        response = {
            'authorized': True
        }
    else:
        print('No idea what this request is')
        response = {
            'authorized': False
        }
    return jsonify(response)



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
    app.debug = True  # NOT to use in PROD - allow the server to reload autonmatically after each change of code
    app.run(host="192.168.1.4",)