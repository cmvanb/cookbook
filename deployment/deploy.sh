#!/bin/bash

#-------------------------------------------------------------------------------
# Deploy cookbook
#
# NOTE: This script is written for deployment on Ubuntu 20.04 (focal) with
# Apache and mod_wsgi.
#-------------------------------------------------------------------------------

# TODO: Take variables from environment.
APP_DIR=/var/www/cookbook
APP_PKG=git+https://github.com/cmvanb/cookbook.git#egg=cookbook
PYTHON=python3.10

WORK_DIR=$(pwd)

# Remove existing deployment.
rm -rf $APP_DIR/*

# Change directory.
cd $APP_DIR

# Create and activate virtual environment.
$PYTHON -m venv venv
source venv/bin/activate

# Ensure latest pip.
venv/bin/pip install --upgrade pip

# Install app.
venv/bin/pip install $APP_PKG

# Initialize database.
venv/bin/flask --app cookbook init-db

# Install WSGI entry point.
cp $WORK_DIR/deployment/wsgi.py $APP_DIR/wsgi.py

# Give ownership to apache.
chown -R www-data:www-data $APP_DIR

# Deactivate virtual environment.
deactivate

# Restart apache.
systemctl restart apache2
