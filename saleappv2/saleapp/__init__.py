from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary
import os
from flask_wtf import FlaskForm, RecaptchaField

app = Flask(__name__)
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/foodappdb?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'
app.config['SECRET_KEY'] = '6LeM0fMkAAAAAPvNj-HkjFpj0FFX7mPfjH44fRpn'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfIq_MkAAAAAAkqaKZUFwqhKnBZ44wfanxQfFQk'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfIq_MkAAAAAFdstbFJGU6u0eHIWttg8n9_d1x3'
cloudinary.config(cloud_name='dhwuwy0to', api_key='569153767496484', api_secret='ghXq0iY8RhWbqBcJaide7W-34RY')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'
