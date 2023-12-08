#!/bin/bash

python manage.py makemigrations
python manage.py migrate

# 使用 QINGJIN_ENV 变量区分生产环境和开发环境
if [ "${QINGJIN_ENV}" = "prod" ]
then
    python manage.py runserver 0.0.0.0:8000
else
    python manage.py runserver
fi
