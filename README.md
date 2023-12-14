# FastPhotoAPI

An efficient, flexible, flask-based image server that uses lanczos resampling to serve optimized cached photos.

```shell
python3.12 -m venv fast_photo_venv
source fast_photo_venv/bin/activate
pip install -r requirements.txt
```


## Usage:
- Fetch a resampled & cached image `/image/<yourimage>`
- Fetch the original, unmodified image `/full/<yourimage>`


## Structure:

This application adopts the factory pattern; `flask run` instantiates the built-in development server by executing `create_app()` at the root of the `app/` package, while `python application.py` creates a new production application, served by waitress. 


```shell
.
├── app
          ├── __init__.py  #  create and serve development application
          └── main
              ├── config
│             │         └── config.cfg  # set directories, max image dimensions, etc
│             ├── fullsize
│             │         └── routes.py  # Blueprint routing for serving verbatim image files 
│             ├── __init__.py  # `create_app()` entrypoint
│             ├── resampled
│             │         ├── model.py  # Image resampling methods
│             │         └── routes.py  # Blueprint routing for `/image/`  
│             └── static
│                 └── routes.py  # Blueprint routing for `/static/` 
├── application.py  # create and serve production application w/ waitress
├── cache  # resampled images are dynamically generated adn stored here 
├── Dockerfile  # currently deployed at Koyeb  
├── pictures # full res pictures go here
├── README.md  # you are here
├── static
│         └── style.css  # index styling
└── templates
    ├── index.html  
    └── upload.html
```

## Build

*Locally:*
```dev server:
flask run # 0.0.0.0:5000
```
```waitress server:
flask run # 0.0.0.0:8000
```

*Production via Docker:*
```shell
## build production docker image:
docker build -t <srv> .

## serve production docker image locally:
docker run -d -p 8000:8000 <srv>:latest

## stop local image:
# docker ps
# docker stop 

## push image to a container registery: 
# docker push <srv>
```
