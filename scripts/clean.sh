#!/bin/bash
#-------------------------------------------------------------------------------
# Clean various development artifacts
#-------------------------------------------------------------------------------

set -euo pipefail

empty_directory() {
    if [[ -d "$1" ]]; then
        rm $1/*
        echo "Emptied $1."
    else
        echo "$1 doesn't exist."
    fi
}

remove_file() {
    if [[ -f "$1" ]]; then
        rm $1
        echo "Removed $1."
    else
        echo "$1 doesn't exist."
    fi
}

user_images_dir=cookbook/static/user_images
database=instance/cookbook.sqlite
coverage_report=.coverage
session_json=session.json

empty_directory $user_images_dir
remove_file $database
remove_file $coverage_report
remove_file $session_json

echo 'clean.sh complete.'
