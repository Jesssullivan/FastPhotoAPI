import os
from flask import Blueprint, request, send_from_directory, make_response, render_template, redirect
from flask import current_app as app
import werkzeug.utils
from .model import generate_picture, get_image_dimensions
from ..config.conf import new_client, new_client_dir
import time

photo_blueprint = Blueprint("photo", __name__)

@photo_blueprint.route("/media/<path:path>")
@photo_blueprint.route("/image/<path:path>")
@photo_blueprint.route("/images/<path:path>")
def send_picture(path):
    usr_id = new_client()
    usr_dir = new_client_dir(usr_id)

    w = request.args.get("w", type=float)
    h = request.args.get("h", type=float)
    
    scale_y = round(w) if w else None
    scale_x = round(h) if h else None
    
    crop = bool(request.args.get("crop"))
    encoding = request.args.get("encoding")

    path, cache_hit = generate_picture(usr_dir, path, scale_x, scale_y, encoding, crop)
    
    raw = send_from_directory(directory="../../", path=path, as_attachment=False, max_age=2592000)
    response = make_response(raw)

    response.headers['X-PICTURE-FACTORY-INTERNAL-FID'] = path
    response.headers['X-PICTURE-FACTORY-INTERNAL-CACHE-HIT'] = cache_hit
    cache_timeout = request.args.get("cache-timeout") or request.args.get("ct") or "3600"
    response.headers['Cache-Control'] = "max-age=" + str(cache_timeout)

    if encoding:
        response.headers['Content-Type'] = f"image/{encoding}"

    return response

@photo_blueprint.route("/")
def photo_list():
    retStringArr = []
    for root, dirs, files in os.walk(app.config['PICTURE_DIR']):
        for f in files:
            retStringArr += [os.path.join(os.path.basename(root), f)]

    isPictureDict = dict()
    for p in retStringArr:
        isPicture = any([x in p.lower() for x in ["jpg", "png", "wep", "svg", "gif", "jpeg"]])
        isPictureDict.update({p: isPicture})

    return render_template("index.html", paths=retStringArr, isPictureDict=isPictureDict)


@photo_blueprint.route("/upload", methods=['GET', 'POST'])
def upload():
    if not app.config['UPLOAD_ENABLED']:
        return "Upload Disabled", 403
    if request.method == 'POST':
        f = request.files['file']
        fname = werkzeug.utils.secure_filename(f.filename)
        sfName = os.path.join(app.config['PICTURE_DIR'], fname)
        if not os.path.isfile(sfName):
            f.save(sfName)
            realHostname = request.headers.get("X-REAL-HOSTNAME")
            if realHostname:
                return redirect("/media/" + fname)
            else:
                return 'Success', 204
        else:
            return 'Conflicting File', 409
    else:
        return render_template("upload.html")


@photo_blueprint.route('/', defaults={'path': ''})
@photo_blueprint.route('/<path:path>')
def yeet(path):
    print('You want path: %s' % path)
    return redirect('/')
