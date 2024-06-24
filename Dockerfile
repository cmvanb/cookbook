#-------------------------------------------------------------------------------
# Dockerfile
#-------------------------------------------------------------------------------

FROM tiangolo/uwsgi-nginx-flask:python3.11

ENV UWSGI_INI=/app/uwsgi.ini
ENV STATIC_URL=/app/app/static

WORKDIR /app
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./cookbook /app/cookbook

RUN pip install -r /app/cookbook/requirements.txt
