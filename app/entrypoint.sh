#!/bin/bash
python manage.py migrate
# python3 manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000