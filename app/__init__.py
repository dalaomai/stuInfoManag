from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    from app.personal import personal as personal_blueprint
    app.register_blueprint(personal_blueprint,url_prefix='/personal')
    from app.course import course 
    app.register_blueprint(course,url_prefix='/course')
    from app.student import student 
    app.register_blueprint(student,url_prefix='/student')
    from app.source import source 
    app.register_blueprint(source,url_prefix='/source')
    from app.teacher import teacher 
    app.register_blueprint(teacher,url_prefix='/teacher')
    from app.admin import admin 
    app.register_blueprint(admin,url_prefix='/admin')
    from app.aclass import aclass 
    app.register_blueprint(aclass,url_prefix='/aclass')

    app.app_context().push()
    return app

