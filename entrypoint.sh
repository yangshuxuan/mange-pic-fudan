#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.
echo "Waiting for MySql to start..."
./wait-for db:3306

python manage.py migrate --noinput

python manage.py runserver 9001
