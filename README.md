#  django-rest-jwt

https://stackpython.co/tutorial/django-rest-framework-api-python

https://dev.to/biplov/function-based-views-vs-class-based-views-django-20ak

## env manage

````
# Create a folder to store our project
mkdir restframework

# ชี้ไปที่โฟลเดอร์ที่สร้างขึ้นมา
cd restframework

# สร้าง virtual environment ชื่อว่า env
virtualenv env

# Activate (เรียกใช้งาน) virtual environment (Windows)
env\Scripts\activate
````

## install django djangorestframework

````
pip install django
pip install djangorestframework

django-admin startproject appmain

cd appmain

python manage.py startapp api
````

pip freeze > requirements.txt

````
asgiref==3.5.2
cffi==1.15.1
cryptography==38.0.1
Django==3.2.16
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.1
pycparser==2.21
PyJWT==2.5.0
pytz==2022.4
sqlparse==0.4.3
typing_extensions==4.3.0

````


nano appmain\appmain\settings.py


````
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',  # Oup app
    'rest_framework'  # DRF
]
````



nano appmain\api\models.py 

````
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField()

    class Meta:
        ordering = ['-date_created']
        db_table = 'task'
    
    def __str__(self):
        return self.title
````

## migrate command

````
python manage.py makemigrations && python manage.py migrate
````


nano appmain\api\serializers.py

````
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'date_created', 'complete')
````


nano appmain\api\views.py 

````
from django.shortcuts import render
from .serializers import TaskSerializer
from .models import Task
from rest_framework import generics


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # return Response(queryset.data)
````

nano appmain\appmain\urls.py 

````
from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', views.TaskList.as_view()),
]
````

## api list

````
 /api/tasks/  		-->  GET 	--> ดึงข้อมูล tasks มาแสดงผลทุก task
 /api/tasks/<id>/   -->  GET  	--> ดึงข้อมูลมาแสดงเฉพาะ task นั้น ๆ 
 /api/tasks/   		-->  POST  	--> สร้าง task ขึ้นมาใหม่
 /api/tasks/<id>/   -->  PUT  	--> อัปเดตข้อมูลใน task นั้น ๆ  
 /api/tasks/<id>/   -->  DELETE  --> ลบ task นั้น ๆ   
````

## create user admin 

````
python manage.py createsuperuser --email admin@example.com --username admin
<ENTER PASSWORD>
<PRESS Y CONFIRM>
````


nano appmain\api\admin.py

````
from django.contrib import admin
from .models import Task

# Register our model
admin.site.register(Task)
````


## test run

````
python manage.py runserver 0.0.0.0:8000
````


nano appmain\api\view.py

````
# add form 
class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# New
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
````


nano appmain\appmain\urls.py 

````
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', views.TaskList.as_view()),
    path('api/tasks/<int:pk>', views.TaskDetail.as_view())  # New
]
````

# Permissions & Authentication

## 

nano appmain\api\views.py

````
from django.shortcuts import render
from .serializers import TaskSerializer
from .models import Task
from rest_framework import generics, permissions


class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] # ADD NEW
    # return Response(queryset.data)


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] # ADD NEW


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # ADD NEW


````

## Login Browsable API

nano appmain\appmain\urls.py

````
urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls'))  # New
]
````


# ADD JWT AUTHEN 

````
pip install djangorestframework-simplejwt
pip install djangorestframework-simplejwt[crypto]
````

nano appmain\appmain\settings.py

````
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}
````

nano appmain\appmain\urls.py

````
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]

````

nano appmain\appmain\urls.py

````
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    ...
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ...
]
````

nano appmain\appmain\settings.py

````
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt',
    ...
]
````

## use

````
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/api/token/

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
````



nano appmain\appmain\settings.py

````
from datetime import timedelta
...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(hours=8),
#    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
````

## CACHE 

````
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
````
