# импортируем стандартные модели джанго
from django.db import models

# импортируем модель клиента
from customers.models import Customer


# модель заказа
class Order(models.Model):
    # описание полей, поле id создается автоматически
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
