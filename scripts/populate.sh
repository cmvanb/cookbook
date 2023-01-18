#!/bin/bash
#-------------------------------------------------------------------------------
# Populate database with demo data
#-------------------------------------------------------------------------------

set -euo pipefail

# TODO: Add usage helper.
# TODO: Parse command line arguments.

# Server configuration.
ADDRESS=127.0.0.1
PORT=5000

# User configuration.
EMAIL=demo@gmail.com
PASSWORD=demo
DISPLAY_NAME=Demo

# Recipes configuration.
RECIPE_DIR=demo_recipes

# Register and login.
http --form POST $ADDRESS\:$PORT/auth/register email=$EMAIL password=$PASSWORD display_name=$DISPLAY_NAME
http --form POST $ADDRESS\:$PORT/auth/login email=$EMAIL password=$PASSWORD

# Add some recipes.
# TODO: Read recipe data files.
# TODO: Post recipe data.

