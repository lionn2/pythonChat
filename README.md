pythonChat
==========

python + js chat


To start this app you have to 
1. install: 
-python 2.7
-django 1.7.1
-mysql or sqlite
2. config /OurChat/settings.py file:
-mysql: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'chat',
            'USER': 'username',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
-sqlite3:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    }
3. create table in database:
-mysql: CREATE DATABASE chat CHARACTER SET utf8;
4. sync django project with db:
  Open the Terminal and cd to 'pythonChat' dir.
  
  execute:
  python manage.py makemigrations chat
  python manage.py migrate
  
5. now you can run the project:
  python manage.py runserver [host[:port]]    #default 127.0.0.1:8000
