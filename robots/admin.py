# импорт админки
from django.contrib import admin

# импорт модели робота
from .models import Robot

# Register your models here.
# добавление модели в админку
admin.site.register(Robot)
