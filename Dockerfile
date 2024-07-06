#-------------------------------------------------------------------------------
# Dockerfile
#-------------------------------------------------------------------------------

FROM tiangolo/uwsgi-nginx-flask:python3.11

ENV FLASK_APP=cookbook:app
ENV STATIC_PATH=/app/cookbook/main/static
ENV UWSGI_INI=/app/uwsgi.ini

WORKDIR /app
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./cookbook /app/cookbook

RUN pip install -r /app/cookbook/requirements.txt
