import os
from PIL.Image import Resampling, open, UnidentifiedImageError
from flask import current_app as app


def generate_picture(path_to_orig, scale_x, scale_y, encoding, crop):

    if os.path.isfile(app.config['CACHE_DIR']):
        raise OSError("Picture cache dir is occupied by a file!")

    if not os.path.isdir(app.config['CACHE_DIR']):
        os.mkdir(app.config['CACHE_DIR'])

    filename, extension = os.path.splitext(os.path.basename(path_to_orig))
    if not encoding:
        encoding = extension.strip(".")

    if encoding.lower() == "jpg":
        encoding = "jpeg"

    try:
        image = open(os.path.join(app.config['PICTURE_DIR'], path_to_orig))
    except FileNotFoundError:
        return None, False
    except UnidentifiedImageError:
        return os.path.join(app.config['PICTURE_DIR'], path_to_orig), False

    x, y = image.size

    try:
        scale_y = min(x)
        scale_x = min(y) / 4
    except TypeError:
        scale_y = y
        scale_x = x

    if x > app.config['MAX_X']:
        scale_factor = app.config['MAX_X'] / x
        print("Scale factor: " + str(scale_factor))
        scale_x = x * scale_factor
        scale_y = y * scale_factor

    # generate new paths #
    newFile = "x-{x}-y-{y}-{fname}.{ext}".format(x=scale_x, y=scale_y, fname=filename, ext=encoding)
    newPath = os.path.join(app.config['CACHE_DIR'], newFile)

    # check for cache
    if os.path.isfile(newPath):
        return newPath, True

    # save image with new size and encoding #
    if image.mode in ("RGBA", "P") and encoding in "jpeg":
        image = image.convert("RGB")

    if crop:
        image.crop((0, 0, scale_x, scale_y), Resampling.LANCZOS)
    else:
        image.thumbnail((scale_x, scale_y), Resampling.LANCZOS)

    image.save(newPath, encoding)

    # strip the STATIC_DIR because we will use send_from_directory for safety #
    REPLACE_ONCE = 1
    return newPath.replace(app.config['PICTURE_DIR'], "", REPLACE_ONCE), False

