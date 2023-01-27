#!/bin/bash
#-------------------------------------------------------------------------------
# Populate database with demo data
#
# Dependencies: `httpie`, `niet`
#-------------------------------------------------------------------------------

set -euo pipefail

# TODO: Add usage helper.
# TODO: Parse command line arguments.

# Detect script directory.
SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

# Server configuration.
ADDRESS=127.0.0.1
PORT=5000

# User configuration.
EMAIL=demo@gmail.com
PASSWORD=demo
DISPLAY_NAME=Demo

# Recipes configuration.
RECIPE_DIR=$HOME/Projects/cookbook/demo-data
SESSION_FILE=$SCRIPT_DIR/session.json

# Register and login.
http --session="./session.json" --form POST $ADDRESS\:$PORT/auth/register email=$EMAIL password=$PASSWORD display_name=$DISPLAY_NAME
http --session="./session.json" --form POST $ADDRESS\:$PORT/auth/login email=$EMAIL password=$PASSWORD

RECIPES=$(find $RECIPE_DIR -name "*.yaml")

# Add some recipes.
for RECIPE_YAML in $RECIPES; do
    IMAGE_FILE_NAME="$(basename $RECIPE_YAML .yaml).jpg"
    IMAGE=$(find $RECIPE_DIR -name $IMAGE_FILE_NAME)

    if [[ ! -f $IMAGE ]]; then
        echo "Could not find $IMAGE"
        exit 1
    fi

    TITLE=$(niet "title" $RECIPE_YAML)
    AUTHOR=$(niet "author" $RECIPE_YAML)
    DESCRIPTION=$(niet "description" $RECIPE_YAML)
    SOURCE_URL=$(niet "source_url" $RECIPE_YAML)
    SERVINGS=$(niet "servings" $RECIPE_YAML)
    PREP_TIME=$(niet "prep_time" $RECIPE_YAML)
    COOK_TIME=$(niet "cook_time" $RECIPE_YAML)
    INGREDIENTS=$(niet "ingredients" $RECIPE_YAML)
    INSTRUCTIONS=$(niet "instructions" $RECIPE_YAML)

    http --session="./session.json" --form POST $ADDRESS\:$PORT/recipes/add title="$TITLE" author="$AUTHOR" \
        description="$DESCRIPTION" source_url="$SOURCE_URL" servings="$SERVINGS" \
        prep_time="$PREP_TIME" cook_time="$COOK_TIME" ingredients="$INGREDIENTS" \
        instructions="$INSTRUCTIONS" image@"$IMAGE"
done

# TODO: Read recipe data files.
# TODO: Post recipe data.

