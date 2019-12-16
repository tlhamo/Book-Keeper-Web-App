from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_pyfile('config.py')

Bootstrap(app)
datab = SQLAlchemy(app)
lman = LoginManager()
lman.init_app(app)
lman.login_view = 'login'

from views import *
from api import *

if __name__ == '__main__':
	app.run()
