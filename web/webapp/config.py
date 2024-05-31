import os
import secrets

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    STATIC_FOLDER = f"{os.getenv('APP_FOLDER')}/webapp/static"
    
    # SECRETS
    SECRET_KEY = os.environ.get("SECRET_KEY", "2345678-1000")
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512" #"bcrypt"
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', "Secr3T-s4|t_pw4d")

    # DATABASE CONNECTION
    
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAIL
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "contato@claudiolelis.com")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtpout.secureserver.net")
    MAIL_PORT = os.environ.get("MAIL_PORT", 465)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "contato@claudiolelis.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "S7P3R-P043RFuL_passw0rd")


    
    #SECURITY_TRACKABLE
    #SECURITY_PASSWORDLESS
    #SECURITY_TWO_FACTOR
    #SECURITY_UNIFIED_SIGNIN
    #SECURITY_WEBAUTHN
    #SECURITY_MULTI_FACTOR_RECOVERY_CODES
    #SECURITY_OAUTH_ENABLE


class LocalDevelopmentConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    #SECURITY_REGISTERABLE = True
    #SECURITY_USERNAME_ENABLE = False
    #SECURITY_USERNAME_REQUIRED = False
    #SECURITY_USERNAME_MIN_LENGTH = 8
    #SECURITY_USERNAME_MAX_LENGTH = 32
    #SECURITY_CHANGEABLE = False
    #SECURITY_SEND_REGISTER_EMAIL = False #default is true

    # SECURITY
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = False #True # enable the change password endpoint.
    SECURITY_SEND_REGISTER_EMAIL = False #True
    SECURITY_CONFIRMABLE = False #True # creates an endpoint to handle confirmations and requests to resend confirmation instructions.
    SECURITY_RECOVERABLE = False #True # create a password reset/recover endpoint.



class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
        user = os.environ.get('DB_USER',"postgres"),
        password = os.environ.get('DB_PASSWORD',"you_may_put_default_password_here"),
        host = os.environ.get('DB_HOST',"localhost"), 
        port = os.environ.get('DB_PORT','5432'),
        db_name = os.environ.get('DB_NAME',"flask_db")
    )

    # SECRETS
    SECRET_KEY = os.environ.get("SECRET_KEY", 'your_production_secret_key_here')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "could_be_created_with_library_secrets")
    #SECURITY_PASSWORD_COMPLEXITY_CHECKER = "zxcvbn"

    # SECURITY
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True # enable the change password endpoint.
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_CONFIRMABLE = True # creates an endpoint to handle confirmations and requests to resend confirmation instructions.
    SECURITY_RECOVERABLE = True # create a password reset/recover endpoint.
