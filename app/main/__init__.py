from flask import Flask, redirect
from .resampled.routes import photo_blueprint
from .static.routes import static_blueprint
from .fullsize.routes import fullsize_blueprint


def create_app(environment=None, start_response=None):

    # Flask Config
    app = Flask(__name__)

    app.config.from_pyfile("config/config.cfg")

    app.config['UPLOAD_EXTENSIONS'] = ["jpg", "png", "wep", "svg", "gif", "jpeg"]

    app.template_folder = "../../templates/"
    app.static_folder = "../../static/"

    # Register Blueprints
    app.register_blueprint(photo_blueprint, url_prefix="/")
    app.register_blueprint(static_blueprint, url_prefix="/static/")
    app.register_blueprint(fullsize_blueprint, url_prefix="/full/")


    return app
