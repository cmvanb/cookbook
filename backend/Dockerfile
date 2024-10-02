FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN pip install --upgrade pip
RUN pip install --no-cache-dir /app

COPY ./app /app/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
