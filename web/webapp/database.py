# database.py
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from sqlalchemy.sql import select
from sqlalchemy import text, select
import time

db = SQLAlchemy()
# migrate = Migrate()



def connect_db_with_retries(app):
    max_retries = app.config.get('DB_MAX_CONNECTION_RETRIES', 5)
    for retry in range(max_retries):
        try:
            with app.app_context():
                db.session.execute(text('SELECT 1'))
                db.session.commit()
            break
        except Exception as e:
            db.session.rollback()
            if retry == max_retries - 1:
                raise e
            else:
                time.sleep(2 ** retry)