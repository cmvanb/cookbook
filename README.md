# Cookbook

A personal recipe management and meal planner app.

## Development

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
flask --app cookbook init-db
```

Run the local development server.

```bash
flask --app cookbook --debug run
```

Navigate to `localhost:5000`.

## Tests

```bash
coverage run -m pytest
coverage report
```

## Docker

Build the image.

```bash
docker build -t cookbook:local .
```

Run the container on port 5000.

```bash
docker run --rm -it -p 5000:80 cookbook:local
```
