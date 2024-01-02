#!/bin/sh

docker exec -it app python manage.py makemessages -l en

docker exec -it app python manage.py makemessages -l ja

docker exec -it app django-admin makemessages -d djangojs -l en

docker exec -it app django-admin makemessages -d djangojs -l ja

docker exec -it app python manage.py compilemessages