#!/usr/bin/python2
import sys
import logging

logging.basicConfig(stream=sys.stderr)

activate_this = "/home/user/neoPyth/env/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

sys.path.insert(0, "/home/user/neoPyth")
from app import app as application
