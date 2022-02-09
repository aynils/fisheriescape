#!/bin/bash
service ssh start
python create_env_file_from_json.py --environment-name "$ENVIRONMENT_NAME" --output-file-name=".env"
python manage.py compilemessages
python manage.py collectstatic --no-input
python manage.py showmigrations
python manage.py migrate
celery -A dm_apps beat -l info --detach
celery -A dm_apps worker -l info --detach
gunicorn -b 0.0.0.0:8000 -c gunicorn.conf.py dm_apps.wsgi:application