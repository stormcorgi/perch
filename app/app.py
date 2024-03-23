from flask import Flask

from app.list import folder, top
from app.play import item


def create_app(config_name):
    app = Flask(__name__)
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(top.blueprint)
    app.register_blueprint(folder.blueprint)
    app.register_blueprint(item.blueprint)
    return app
