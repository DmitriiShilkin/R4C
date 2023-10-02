# импорт стандартных моделей джанго
from django.db import models


# модель клиента
class Customer(models.Model):
    # поле модели, поле id создается автоматически
    email = models.CharField(max_length=255, blank=False, null=False)
