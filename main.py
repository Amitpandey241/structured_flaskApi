from app import app
from flask import Blueprint
from app.master.views import example_blueprint
from logging import FileHandler,WARNING

app.register_blueprint(example_blueprint)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
