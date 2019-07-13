import os
try:
    from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
except ImportError:
    from cherrypy.wsgiserver import CherryPyWSGIServer as WSGIServer, WSGIPathInfoDispatcher as PathInfoDispatcher

from app.run import app


HOST_PORT = os.environ.get("HOST_PORT",8000)
d = PathInfoDispatcher({'/': app})
server = WSGIServer(('0.0.0.0', HOST_PORT), d)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
