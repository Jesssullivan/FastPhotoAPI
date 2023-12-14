
FROM python:3.12-alpine

# upgrade pip
RUN pip install --upgrade pip


WORKDIR /srv


# copy all the files to the container
COPY . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN export FLASK_APP=application.py
RUN pip install -r requirements.txt
COPY . .

# define the port number the container should expose
EXPOSE 80

CMD ["python", "application.py"]
