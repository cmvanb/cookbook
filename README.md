# Cookbook

A personal recipe management and meal planner app.

## Development

![Build](https://github.com/cmvanb/cookbook/actions/workflows/docker.yml/badge.svg)
![Test](https://github.com/cmvanb/cookbook/actions/workflows/test.yml/badge.svg)

1. Install the project.

```bash
git clone git@github.com:cmvanb/cookbook.git
cd cookbook
python -m venv venv
source venv/bin/activate
pip install -r cookbook/requirements.txt
```

2. Initialize the database.

```bash
FLASK_APP=cookbook:app flask init-db
```

3. Run the local development server.

```bash
FLASK_APP=cookbook:app flask --debug run
```

4. Use `localhost:5000`.

## Tests

1. Run the tests.

```bash
coverage run -m pytest
```

2. Generate a coverage report.

```bash
coverage report
```

## Docker

1. Copy `example.env` and rename it to `.env`.

```bash
cp example.env .env
```

2. Edit the `.env` file to set the Flask secret key.

3. Build and run the image.

```bash
docker compose up --build
```

4. Use `localhost:5000`.
