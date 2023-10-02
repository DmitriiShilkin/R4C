# импорт библиотеки для работы с JSON
import json
# импорт инструментов для работы с запросами
from django.http import JsonResponse
# импорт стандартного представления
from django.views import View

# импорт модели робот
from .models import Robot


# представление для создания роботов через API
class RobotsAPIView(View):

    def post(self, request):
        # сохраняем тело запроса
        post_body = json.loads(request.body)
        # извлекаем из тела запроса нужные данные
        robot_model = post_body.get('model')
        robot_version = post_body.get('version')
        robot_serial = f"{robot_model}-{robot_version}"
        robot_created = post_body.get('created')
        # создаем JSON
        robot_data = {
            'serial': robot_serial,
            'model': robot_model,
            'version': robot_version,
            'created': robot_created,
        }
        # создаем экземпляр объекта модели
        robot_obj = Robot(**robot_data)
        # проводим валидацию введенных значений
        robot_obj.full_clean()
        # сохраняем экземпляр в БД
        robot_obj.save()
        # сообщение при успешном создании
        data = {'message': f'Новый робот создан с id {robot_obj.id}'}
        return JsonResponse(data, status=201)
