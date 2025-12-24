#!/bin/bash
# ضبط البورت، لو Railway مديه استخدمه، لو لأ استخدم 8000
export PORT=${PORT:-8000}

# تنفيذ أي تغييرات على قاعدة البيانات
python manage.py migrate

# تجميع ملفات static (مهم لو عندك static files)
python manage.py collectstatic --noinput

# تشغيل السيرفر على كل IPs والبورت اللي Railway مديه
python manage.py runserver 0.0.0.0:$PORT
