# Cookbook

A personal recipe management and meal planner app.

## Development

![Build](https://github.com/cmvanb/cookbook/actions/workflows/build.yml/badge.svg)
![Test](https://github.com/cmvanb/cookbook/actions/workflows/test.yml/badge.svg)

Install the project.

```bash
git clone git@github.com:cmvanb/cookbook.git
cd cookbook
python -m venv venv
source venv/bin/activate
pip install -r cookbook/requirements.txt
```

Initialize the database.

```bash
FLASK_APP=cookbook:app flask init-db
```

Run the local development server.

```bash
FLASK_APP=cookbook:app flask --debug run
```

Use `localhost:5000`.

## Tests

```bash
coverage run -m pytest
coverage report
```

## Docker

With compose:

```bash
docker compose up --build
```

Use `localhost:5000`.
