@echo off
cd /d D:\Compilers\VSC-Folders\Django_Projects\Event Countdown\core
call venv\Scripts\activate
start http://127.0.0.1:8000
python manage.py runserver
