#!/bin/sh
set -e

# Ждём базу
/app/wait-for-db.sh db 5432

# Запускаем миграции
python manage.py migrate

# Запускаем тесты
pytest --cov=. --cov-report=term-missing
