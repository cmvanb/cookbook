# Cookbook

A personal recipe management and meal planner app.

## Development

1. Install backend dependencies.

```bash
cd backend
pip install .
```

2. Run the app in development mode.

```bash
fastapi dev app/main.py
```

3. Navigate to `http://localhost:8000`.

## Docker

1. Build the Docker image.

```bash
cd backend
docker build -t cookbook:local .
```

2. Run the Docker container.

```bash
docker run --rm -it -p 8000:80 cookbook:local
```

3. Navigate to `http://localhost:8000`.
