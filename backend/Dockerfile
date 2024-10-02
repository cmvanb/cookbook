FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./app /app/app

RUN pip install .

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
