#!/bin/bash

echo "Применяем миграции"
python manage.py migrate

echo "Запускаем фикстуры"
python manage.py loaddata fixtures/*

echo "Запуск сервера"
python manage.py runserver 0.0.0.0:8000