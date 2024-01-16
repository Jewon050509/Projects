from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# Create Flask application
def create_app():
    from .views import views
    from .auth import auth
    from .models import User

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Jewon'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# Creates database if it does not exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)