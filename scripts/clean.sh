#!/bin/bash
#-------------------------------------------------------------------------------
# Clean various development artifacts
#-------------------------------------------------------------------------------

set -euo pipefail

# Empty directories.
#-------------------------------------------------------------------------------
declare -a dirs=(
    "cookbook/static/user_images"
)

for dir in "${dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        rm "$dir"/*
        echo "Emptied $dir."
    fi
done

# Remove directories.
#-------------------------------------------------------------------------------
declare -a dirs=(
    ".pytest_cache"
)

for dir in "${dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        rm -r "$dir"
        echo "Removed $dir."
    fi
done

# Remove files.
#-------------------------------------------------------------------------------
declare -a files=(
    "instance/cookbook.sqlite"
    ".coverage"
    "session.json"
)

for file in "${files[@]}"; do
    if [[ -f "$file" ]]; then
        rm "$file"
        echo "Removed $file."
    fi
done

echo 'clean.sh complete.'
