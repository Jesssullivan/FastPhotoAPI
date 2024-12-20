import os
import time
import secrets


verbose = False



# uploaded files are placed in temporary server side directories:
live_app_list = {}
start_time = time.time()


# how often should the garbage collector remove old directories?
collection_int = 60 * 30   # secs
collection_trash = 60 * 30  # secs

# recyclable serverside directories-

# serverside paths:
rootpath = os.path.abspath(os.curdir)

# temporary user directories go in here:
inpath = os.path.join(rootpath, 'cache')


# placeholders for usr hash:
usr_id = ''


def new_client():
    return secrets.token_hex(15)


def new_client_dir(usrid):
    usr_dir = os.path.join(inpath, usrid)
    return usr_dir


def vprint(text):
    if verbose:
        print(text)