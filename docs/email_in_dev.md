To mock or fake an email service for testing and demonstration purposes, you have a few options. These options allow you to demonstrate that the email functionality works without actually sending real emails. Here are some common approaches:

### 1. Using `Flask-Mail` with a Dummy SMTP Server

You can use a dummy SMTP server that captures emails instead of sending them. `Flask-Mail` can be configured to use a local development SMTP server like [MailHog](https://github.com/mailhog/MailHog) or [smtp4dev](https://github.com/rnwood/smtp4dev).

#### Using MailHog

##### Step 1: Add MailHog to Docker Compose

Add a MailHog service to your `docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  lelis-web:
    build:
      context: ./web
      dockerfile: Dockerfile.dev
    command: gunicorn -w 2 --bind 0.0.0.0:5000 --timeout 60 -k eventlet --log-level=debug --access-logfile=- app:app
    ports:
      - 8888:5000
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
      - APP_FOLDER=/home/app/web
      - FLASK_SECRET_KEY=very-powerful-sEcr3t-KeY
      - DB_USER=teste_claudiolelis
      - DB_PASSWORD=P4SSw0rd-test-000000
      - DB_HOST=postgres-db
      - DB_PORT=5432
      - DB_NAME=teste_claudiolelis_db
      - MAIL_SERVER=mailhog
      - MAIL_PORT=1025
      - MAIL_USE_TLS=false
      - MAIL_USE_SSL=false
      - MAIL_USERNAME=null
      - MAIL_PASSWORD=null
    container_name: lelis-web
    networks:
      - postgres-network
    volumes:
      - ./web/webapp/templates:/home/app/web/webapp/templates
    depends_on:
      - postgres-db
      - mailhog

  postgres-db:
    image: postgres:16.1-alpine3.19
    environment:
      POSTGRES_USER: teste_claudiolelis
      POSTGRES_PASSWORD: P4SSw0rd-test-000000
      POSTGRES_DB: teste_claudiolelis_db
    ports:
      - 5433:5432
    container_name: postgres-db
    hostname: postgres-db
    networks:
      - postgres-network
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mailhog:
    image: mailhog/mailhog
    ports:
      - 8025:8025
      - 1025:1025
    container_name: mailhog
    networks:
      - postgres-network

networks:
  postgres-network:
    name: postgres-network

volumes:
  postgres_data:
```

##### Step 2: Configure Flask-Mail

Update your `create_app` function to configure Flask-Mail using the MailHog settings:

```python
# webapp/__init__.py

from flask import Flask, render_template
import os
import logging
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_mailman import Mail
from .config import LocalDevelopmentConfig, ProductionConfig
from .models import User, Role
from .database import db, connect_db_with_retries

def create_app():
    app = Flask(__name__)

    env_ = os.environ.get('FLASK_ENV', "development")
    if env_ == "production":
        print("++///---------Starting Production Development----------///++".upper())
        app.config.from_object(ProductionConfig)
    else:
        print("++///---------Starting Local Development----------///++".upper())
        app.config.from_object(LocalDevelopmentConfig)

    user = os.environ.get('DB_USER', 'teste_user')
    password = os.environ.get('DB_PASSWORD', 'teste_password')
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)
    db_name = os.environ.get('DB_NAME', 'teste_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SECURITY_PASSWORD_HASH'] = "pbkdf2_sha512"
    app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_secret'
    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = "security/login_user.html"
    app.config['SECURITY_REGISTER_USER_TEMPLATE'] = "security/register_user.html"
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
            'application_name': 'flask-app',
        },
    }

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 25))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'false').lower() in ['true', '1', 't']
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', None)
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', None)

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    mail = Mail(app)

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    @app.route('/home/', methods=['GET', 'POST'])
    @auth_required()
    def bp_home():
        return render_template('home_new.html')

    from .bp_list_reports import report_list
    app.register_blueprint(report_list)

    connect_db_with_retries(app)

    return app
```

### 2. Using Flask-Mail with Console Backend

Another approach is to use Flask-Mail’s console backend for development. This backend prints the email content to the console instead of sending it.

#### Step 1: Configure Flask-Mail

Configure Flask-Mail in your `create_app` function to use the console backend:

```python
# webapp/__init__.py

from flask import Flask, render_template
import os
import logging
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_mailman import Mail
from .config import LocalDevelopmentConfig, ProductionConfig
from .models import User, Role
from .database import db, connect_db_with_retries

def create_app():
    app = Flask(__name__)

    env_ = os.environ.get('FLASK_ENV', "development")
    if env_ == "production":
        print("++///---------Starting Production Development----------///++".upper())
        app.config.from_object(ProductionConfig)
    else:
        print("++///---------Starting Local Development----------///++".upper())
        app.config.from_object(LocalDevelopmentConfig)

    user = os.environ.get('DB_USER', 'teste_user')
    password = os.environ.get('DB_PASSWORD', 'teste_password')
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)
    db_name = os.environ.get('DB_NAME', 'teste_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SECURITY_PASSWORD_HASH'] = "pbkdf2_sha512"
    app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_secret'
    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = "security/login_user.html"
    app.config['SECURITY_REGISTER_USER_TEMPLATE'] = "security/register_user.html"
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
            'application_name': 'flask-app',
        },
    }

    # Flask-Mail configuration for development
    if

 env_ == "development":
        app.config['MAIL_BACKEND'] = 'console'

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    mail = Mail(app)

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    @app.route('/home/', methods=['GET', 'POST'])
    @auth_required()
    def bp_home():
        return render_template('home_new.html')

    from .bp_list_reports import report_list
    app.register_blueprint(report_list)

    connect_db_with_retries(app)

    return app
```

With this configuration, emails will be printed to the console during development, allowing you to see that they are being "sent" without actually sending them.

### 3. Using Flask-Mailman with a Fake SMTP Server

If you are using `flask-mailman`, you can use a similar approach with a fake SMTP server.

```python
# webapp/__init__.py

from flask import Flask, render_template
import os
import logging
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_mailman import Mail
from .config import LocalDevelopmentConfig, ProductionConfig
from .models import User, Role
from .database import db, connect_db_with_retries

def create_app():
    app = Flask(__name__)

    env_ = os.environ.get('FLASK_ENV', "development")
    if env_ == "production":
        print("++///---------Starting Production Development----------///++".upper())
        app.config.from_object(ProductionConfig)
    else:
        print("++///---------Starting Local Development----------///++".upper())
        app.config.from_object(LocalDevelopmentConfig)

    user = os.environ.get('DB_USER', 'teste_user')
    password = os.environ.get('DB_PASSWORD', 'teste_password')
    host = os.environ.get('DB_HOST', 'localhost')
    port = os.environ.get('DB_PORT', 5432)
    db_name = os.environ.get('DB_NAME', 'teste_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SECURITY_PASSWORD_HASH'] = "pbkdf2_sha512"
    app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_secret'
    app.config['SECURITY_LOGIN_USER_TEMPLATE'] = "security/login_user.html"
    app.config['SECURITY_REGISTER_USER_TEMPLATE'] = "security/register_user.html"
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
            'application_name': 'flask-app',
        },
    }

    # Flask-Mailman configuration for development
    app.config['MAIL_BACKEND'] = 'locmem'

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    mail = Mail(app)

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/home', methods=['GET', 'POST'])
    @app.route('/home/', methods=['GET', 'POST'])
    @auth_required()
    def bp_home():
        return render_template('home_new.html')

    from .bp_list_reports import report_list
    app.register_blueprint(report_list)

    connect_db_with_retries(app)

    return app
```

### Conclusion

By using one of these methods, you can demonstrate the email functionality in your Flask application without needing to send real emails. This can be particularly useful in development and testing environments. Each method provides a way to capture and view the email content, ensuring that your end-to-end functionality works as expected.

## More details about Approach 2 and 3:

### Approach 2: Flask-Mail with Console Backend

When you use the console backend for Flask-Mail, the emails are printed directly to the console (standard output). Therefore, if you're running your application in a Docker container, you can view the emails by checking the Docker container logs.

To view the Docker logs, you can use the following command:

```sh
docker logs <container_name>
```

For your setup, the container name for your Flask application is `lelis-web`. Therefore, you can view the logs (and thus the emails) with:

```sh
docker logs lelis-web
```

This will display all the logs, including the email content printed by Flask-Mail when an email is "sent."

### Approach 3: Flask-Mailman with Locmem Backend

When you use the `locmem` (in-memory) backend for Flask-Mailman, emails are stored in an in-memory list. This backend is useful for testing purposes but does not provide an out-of-the-box way to view the emails like the console backend does.

To access the emails sent using the `locmem` backend, you need to retrieve them from the in-memory storage. You can do this within your Flask application or within your test cases. Here’s how you can access the emails:

1. **Within Your Flask Application:**
   You can create a route to display the emails stored in memory for debugging purposes.

   ```python
   from flask import Flask, render_template_string
   from flask_mailman import Mail, email_dispatched

   app = Flask(__name__)
   mail = Mail(app)

   emails = []

   def store_email(message, app):
       emails.append(message)

   email_dispatched.connect(store_email)

   @app.route('/debug-emails')
   def debug_emails():
       email_contents = [email.body for email in emails]
       return render_template_string("<br>".join(email_contents))

   if __name__ == "__main__":
       app.run(debug=True)
   ```

   With this route (`/debug-emails`), you can access the emails by visiting `http://localhost:5000/debug-emails` in your browser.

2. **Within Your Test Cases:**
   If you are running tests, you can directly access the `emails` list to check the email content.

   ```python
   def test_email_sending(client, app):
       response = client.post('/send-email', data={...})
       assert response.status_code == 200
       assert len(emails) == 1
       assert 'Expected email content' in emails[0].body
   ```

### Summary

- **Approach 2:** Emails are printed to the console. Check Docker logs using `docker logs lelis-web`.
- **Approach 3:** Emails are stored in memory. You can create a route to display them or access them directly in your test cases.

Both approaches ensure that you can see the email content without sending real emails, making it easier to verify that your email functionality is working correctly.

And, Yes, both approaches will work properly with flask-security-too for features such as user registration, password reset, and other functionalities that involve sending emails. 