import eventlet
eventlet.monkey_patch()

from flask import Flask
from webapp import create_app

app: Flask = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)