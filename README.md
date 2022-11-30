# Cookbook

A personal recipe management and meal planner app

```bash
sudo venv/bin/pip install git+https://github.com/cmvanb/cookbook.git#egg=cookbook
```

## Deployment

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
