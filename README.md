
## Для начала работы с проектом необходимо:
1. Создать и активировать виртуальное окружение 
2. Установить зависимости из requirements.txt : "pip install -r requirements.txt"
3. Создать базу данных
4. Создать файл .env на основе .env_exmpl с вашими данными почты, базы данных
5. Выполнить миграции: "python manage.py makemigrations, python manage.py migrate"
6. Запустить проект
7. Запустить рассылку командой "python manage.py sending_mail_command"




