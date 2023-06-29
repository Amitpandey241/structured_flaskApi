from app import app
from flask import Blueprint
from app.master.views import example_blueprint

app.register_blueprint(example_blueprint)
if __name__ == "__main__":
    app.run(host="0.0.0.0")

