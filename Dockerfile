#-------------------------------------------------------------------------------
# Dockerfile
#-------------------------------------------------------------------------------

FROM tiangolo/uwsgi-nginx-flask:python3.11

ENV FLASK_APP=cookbook:app
ENV UWSGI_INI=/app/uwsgi.ini
# NOTE: This variable is used by the base docker image to configure where static
# files are served from. It is not the same as the STATIC_FOLDER configuration
# variable, although it serves the same purpose.
ENV STATIC_PATH=/app/cookbook/main/static

WORKDIR /app
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./cookbook /app/cookbook

RUN pip install -r /app/cookbook/requirements.txt
