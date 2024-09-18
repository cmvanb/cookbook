# Cookbook

A personal recipe management and meal planner app.

## Demo

A demo of the app is available at [cookbook.codemu.ch](https://cookbook.codemu.ch). You will need to register a user account to access it.

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

4. Alternatively, use the docker dev deployment.

```bash
docker compose -f deployment/dev.yml up --build
```

5. Navigate to `localhost:5000`.

## Tests

1. Run the tests.

```bash
coverage run -m pytest
```

2. Generate a coverage report.

```bash
coverage report
```

## Deployment with Docker

1. Copy `example.env` and rename it to `.env`.

```bash
cp deployment/example.env deployment/.env
```

2. Edit the `.env` file to set the Flask secret key.

3. Build and run the image.

```bash
docker compose -f deployment/demo.yml up --build
```
