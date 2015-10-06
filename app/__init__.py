from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os
from flask.ext.login import LoginManager
#from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)

# app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
#oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models
#from app import views

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello from Flask!'





#from momentjs import momentjs
#app.jinja_env.globals['momentjs'] = momentjs
