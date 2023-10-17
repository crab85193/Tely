#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 環境変数のDEBUGの値がTrueの時はrunserverを、Falseの時はgunicornを実行します
if [ $DEBUG = "True" ]
then
    python manage.py runserver 0.0.0.0:8000
else
    # gunicornを起動させる時はプロジェクト名を指定します
    # 今回はdjangopjにします
    gunicorn djangopj.wsgi:application --bind 0.0.0.0:8000
fi

