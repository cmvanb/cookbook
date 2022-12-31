# Cookbook

A personal recipe management and meal planner app.

A [demo instance](https://codemu.ch/cookbook) is now live.

## Development

```bash
git clone git@github.com:cmvanb/cookbook.git
cd cookbook
python -m venv venv
source venv/bin/activate
flask --app cookbook init-db
flask --app cookbook --debug run
```

Navigate to `127.0.0.1:5000`.

## Tests

```bash
coverage run -m pytest
coverage report
```

## Package Installation

```bash
venv/bin/pip install git+https://github.com/cmvanb/cookbook.git#egg=cookbook
```

## Deployment

Host running `Ubuntu 20.04` with `python3.10`, `sqlite 3.40`, `Apache 2.4` and `mod_wsgi` configured.

```bash
mkdir cookbook
cd cookbook
git init
git sparse-checkout init
git sparse-checkout set deployment
git remote add origin git@github.com:cmvanb/cookbook.git
git fetch --depth=1
git pull origin master
sudo deployment/deploy.sh
```
