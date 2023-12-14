
from flask import Blueprint, request, send_from_directory, make_response, render_template, redirect
from flask import current_app as app


static_blueprint = Blueprint("static", __name__)


# Index Routes:
@static_blueprint.route("/<p>")
def index(p):
    return send_from_directory(app.static_folder, p)
