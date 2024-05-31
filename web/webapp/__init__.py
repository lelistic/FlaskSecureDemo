
# built-in bibs
import os
import logging

# external bibs
from flask import Flask, render_template
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required
)
from flask_mailman import Mail



# project imports
from .config import LocalDevelopmentConfig, ProductionConfig
from .database import db, connect_db_with_retries
# from .database import migrate
from .models import User, Role


logging.basicConfig(level=logging.DEBUG)


def create_app():


    app = Flask(__name__)

    env_ = os.environ.get('FLASK_ENV', "development")
    if env_ == "production":
        print("++///---------Starting Production Development----------///++".upper())
        app.config.from_object(ProductionConfig)
    else:
        print("++///---------Starting Local Development----------///++".upper())
        app.config.from_object(LocalDevelopmentConfig)
        # Flask-Mailman configuration for development
        app.config['MAIL_BACKEND'] = 'console'
        

    user = os.environ.get('DB_USER', 'teste_user')
    password = os.environ.get('DB_PASSWORD', 'teste_password')
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)  # Use 5432 as the default port if DB_PORT is not set
    db_name = os.environ.get('DB_NAME', 'teste_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SECURITY_PASSWORD_HASH'] = "pbkdf2_sha512" #"bcrypt"
    app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_secret'

    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = "security/login_user.html" # Specifies the path to the template for the user login page.

    app.config['SECURITY_REGISTER_USER_TEMPLATE'] = "security/register_user.html" # Specifies the path to the template for the user registration page.

    app.config['SECURITY_USERNAME_ENABLE'] = True
    app.config['SECURITY_USERNAME_REQUIRED'] = True

    app.config['SECURITY_POST_REGISTER_VIEW'] = "/login"
    app.config['SECURITY_POST_LOGIN_VIEW'] = "/home"
    app.config['SECURITY_POST_LOGOUT_VIEW'] = "/login"
    app.config['SECURITY_LOGOUT_METHODS'] = None

    logger = logging.getLogger(__name__)
    logger.warning(app.config['SQLALCHEMY_DATABASE_URI'])


    # SQLAlchemy configuration with connection retries and pooling options
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
        'pool_timeout': 10,
        'max_overflow': 10,
        'pool_size': 5,
        'connect_args': {
            'application_name': 'FlaskSecureDemo-ClaudioLelis',
        },
    }

    db.init_app(app)
    #migrate.init_app(app, db)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    mail = Mail(app)

    ### BLUEPRINTS BEGIN ###

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    @app.route('/home/', methods=['GET', 'POST'])
    @auth_required()
    def bp_home():
        return render_template('home_new.html')

    from .bp_list_reports import list_reports
    app.register_blueprint(list_reports)

    ### BLUEPRINTS END ###
    with app.app_context():
        connect_db_with_retries(app)
    

    return app
