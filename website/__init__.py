from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from os import path

# Database init.
db = SQLAlchemy()

DB_NAME = 'db.sql'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'CY54QNJS31Y8'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    # Views imports.
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    # Models imports.
    from .models import User, Note

    # Database creation.
    create_database(app)

    # Login config.
    login_manager = LoginManager()

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Path where database is created.
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)

        print('Database created')