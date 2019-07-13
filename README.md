# NHS server app for NHS-UI client

### Install the requirements
```pip install -r requirements.txt```

### make sure nhs-ui statics point to the correct folders
otherwise jinja2 templates won't be found.

In run.py:
```app = Flask(__name__,
            static_url_path='',
            static_folder = "<root folder>/nhs-ui/dist",
            template_folder = "<root folder>/nhs-ui/dist")
````

####SWGI:
  * Cherrypy
  
#### WebServer
  * nginx
  