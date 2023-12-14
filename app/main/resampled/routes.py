import os
from flask import Blueprint, request, send_from_directory, make_response, render_template, redirect
from flask import current_app as app
import werkzeug.utils
from .model import generate_picture

photo_blueprint = Blueprint("photo", __name__)


@photo_blueprint.route("/media/<path:path>")
@photo_blueprint.route("/image/<path:path>")
@photo_blueprint.route("/images/<path:path>")
def send_picture(path):

    max_age = 2592000

    y1 = request.args.get("scaley")
    x1 = request.args.get("scalex")
    y2 = request.args.get("y")
    x2 = request.args.get("x")

    # check variables #
    scaleY, scaleX = (None, None)
    if y1:
        scaleY = round(float(y1))
    elif y2:
        scaleY = round(float(y2))

    if x1:
        scaleX = round(float(x1))
    elif x2:
        scaleX = round(float(x2))

    pathDebug = path

    encoding = request.args.get("encoding")
    path, cacheHit = generate_picture(path, scaleX, scaleY, encoding,
                                      bool(request.args.get("crop")))

    print('received path: ' + path + ' to render')
    if not path:
        return "File not found: {}".format(os.path.join('.', pathDebug)), 404

    raw = send_from_directory("../../", path, max_age=max_age)
    response = make_response(raw)

    response.headers['X-PICTURE-FACTORY-INTERNAL-FID'] = path
    response.headers['X-PICTURE-FACTORY-INTERNAL-CACHE-HIT'] = cacheHit

    # check for a cacheTimeout #
    cacheTimeout = request.args.get("cache-timeout")
    if not cacheTimeout:
        cacheTimeout = request.args.get("ct")
    if cacheTimeout:
        response.headers['Cache-Control'] = "max-age=" + str(cacheTimeout)
    else:
        response.headers['Cache-Control'] = "max-age=" + "3600"

    if encoding:
        response.headers['Content-Type'] = "image/{}".format(encoding)

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
