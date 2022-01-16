# setup for flask app
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy()  # init db
DB_NAME = 'database.db'

# creates the flask app
def create_app():
    app = Flask(__name__)
    # for session cookies and other info
    app.config['SECRET_KEY'] = 'secret key for cookies'
    # creat the db and configure it
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # init db with current app

    # import blueprints
    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # we want to run or get the db before UI
    from .models import User, Question, Answer, Rating
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # loads user by the id that is passed in
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
