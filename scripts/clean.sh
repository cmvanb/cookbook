#!/bin/bash

database=instance/cookbook.sqlite
user_images_dir=cookbook/static/user_images

if [[ -f "$database" ]]; then
    rm $database
    echo "Removed $database."
else
    echo "$database doesn't exist."
fi

if [[ -d "$user_images_dir" ]]; then
    rm $user_images_dir/*
    echo "Emptied $user_images_dir."
else
    echo "$user_images_dir doesn't exist."
fi

echo 'clean.sh complete.'


