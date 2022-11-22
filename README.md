# Reddit-Backend

### Steps to run it on LocalHost:
1. mkvirtualenv better-reddit
2. workon better-reddit
3. pip install -r requirements.txt
4. psql -f create-datebase.sql
5. python manage.py runserver

##### Update Models changes:
1. python manage.py makemigration
2. python manage.py migrate

##### Update module changes:
3. pip freeze > requirements.txt

