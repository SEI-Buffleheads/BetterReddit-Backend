# Reddit-Backend

##### Steps to run it on LocalHost:
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


## Routes

##### Only for Admin, Get an array of all users
```
http://127.0.0.1:8000/api/user/
```

##### Get User's Profile
```
http://127.0.0.1:8000/api/user/1/
```

##### Get All Post or Comments
```
http://127.0.0.1:8000/api/posts/
http://127.0.0.1:8000/api/comments/
```

##### CRUD for single Post or Comment
```
http://127.0.0.1:8000/api/posts/1/
http://127.0.0.1:8000/api/comments/1/
```

##### Login
Enter Username and Password
```
localhost:8000/api/auth/login/
```

##### Sign Up
Enter Username and Password
```
localhost:8000/api/auth/register/
```

##### For Login and Sign up Example:
```
{
    "password": "Password123!@",
    "username": "testuser3"
}
```

##### Change PW
Enter old and New Password
```
localhost:8000/api/auth/changePW/6/
```
##### Example:
```
{
    "old_password": "12345678",
    "password": "Password123!@"
}
```
##### Refresh Token
```
localhost:8000/api/auth/refresh/
```
