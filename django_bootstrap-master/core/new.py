# First, create a new Django project
# django-admin startproject todo_project
# cd todo_project
# python manage.py startapp todo_app

# todo_project/settings.py (add 'todo_app' to INSTALLED_APPS)
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'todo_app',
# ]

# todo_app/models.py
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title




# Create a directory: todo_app/templates/todo_app/

# todo_app/templates/todo_app/index.html
# Create this file with the following content:
'''

'''

# After creating all these files, run:
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver