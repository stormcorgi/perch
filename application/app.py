from flask import Flask

from application.list import folder, top

# from application.rest import room


def create_app(config_name):
    app = Flask(__name__)
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)
    app.register_blueprint(folder.blueprint)
    app.register_blueprint(top.blueprint)
    return app
