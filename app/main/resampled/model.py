import os
from time import sleep

from PIL.Image import Resampling, open, UnidentifiedImageError
from flask import current_app as app

def get_image_dimensions(image_path):
    with open(image_path) as img:
        width, height = img.size
        return width, height
    
def generate_picture(usr_dir, path_to_orig, scale_w, scale_h, encoding, crop):
    
    intended_path = os.path.relpath(os.path.join(app.config['CACHE_DIR'], usr_dir).__str__())
    print('top intended_path: ' + intended_path)
    filename, extension = os.path.splitext(os.path.basename(path_to_orig))

    if not encoding:
        encoding = extension.strip(".")

    if encoding.lower() == "jpg":
        encoding = "jpeg"
        
    new_file = "w-{w}-h-{h}-{fname}.{ext}".format(w=scale_w, h=scale_h, fname=filename, ext=encoding)
    new_path = os.path.join(intended_path, new_file)
    
    # # check for cache
    if os.path.isfile(new_path):
        print('found image in usr_dir cache')
        return new_path, True
    else:
        for root, dirs, files in os.walk(app.config['CACHE_DIR']):
            for filename in files:
                if filename == new_file:
                    print('found image in alt usr_dir cache')                
                    print('returning path %s' % os.path.join(root, filename))
                    return os.path.join(root, filename), True
    

    if not os.path.isdir(intended_path):
        os.mkdir(intended_path)

    try:
        image = open(os.path.join(app.config['PICTURE_DIR'], path_to_orig))
    except FileNotFoundError:
        return None, False
    except UnidentifiedImageError:
        return os.path.join(app.config['PICTURE_DIR'], path_to_orig), False
    
    # handle partial scale args:
    width, height = image.size
    
    if not scale_w and not scale_h:
        print('sending full image, no args provided')
        return os.path.join(app.config['PICTURE_DIR'], path_to_orig), False
    elif not scale_w and scale_h:
        scale_w = width * (height / scale_h)
    elif not scale_h and scale_w:
        scale_h = height * (width / scale_w)
        
    # save image with new size and encoding #
    if image.mode in ("RGBA", "P") and encoding in "jpeg":
        image = image.convert("RGB")

    if crop:
        print('doing crop')        
        image = image.crop((0, 0, scale_w, scale_h))
    else:
        print('doing thumbnail')
        image.thumbnail((scale_w, scale_h), Resampling.LANCZOS)

    image.save(new_path, encoding)
    image.close()
    print('returning net_path: ' + new_path)

    # strip the STATIC_DIR because we will use send_from_directory for safety 
    return new_path, False
    
    
