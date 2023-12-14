from flask import Blueprint, send_from_directory
from flask import current_app as app
import os

fullsize_blueprint = Blueprint("fullsize", __name__)


@fullsize_blueprint.route("/<p>")
def fullsend(p):
    return send_from_directory(os.path.abspath(app.config['PICTURE_DIR']), p)
