import os

_basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(_basedir, 'uploads/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

DEBUG = False
LOGFILE = 'server.log'

# os.urandom(24)
SECRET_KEY = '{h\xb6\r\t\xf0\x06\x94n\x04\x1c\xc1F#\xf8\xcf\xc4\x04\x8c\rx\xd1\x1a\xc9'
NEO4J_HOST = 'localhost:7474'
NEO4J_USER = 'neo4j'
NEO4J_PASS = 'qwerty'


THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = "something_random"