# импорт сигнала на событие создания новой записи
from django.db.models.signals import post_save

# импорт декоратора, который позволяет функции срабатывать по событию
from django.dispatch import receiver

# импорт моделей заказа и робота
from .models import Order
from robots.models import Robot

# импорт функции отправки почты
from .tasks import send_mails


# отправка уведомления на эл. почту при появлении нового робота, на которого есть заказ
@receiver(post_save, sender=Robot)
def post_add_notification(sender, instance, created, **kwargs):
    # если запись создана
    if created:
        # получаем серийный номер робота
        serial = instance.serial
        # считаем количество роботов
        count = Robot.objects.filter(serial=serial).count()
        # если роботов с таким серийным номером не было и появился первый
        if count == 1:
            # здесь будут собраны эл. адреса клиентов, кто заказал такого робота
            customers_emails = set()
            # находим заказы на этого робота
            orders = Order.objects.filter(robot_serial=serial)
            # пробегаемся по всем заказам
            for order in orders:
                # и собираем адреса эл. почты клиентов
                customers_emails.add(order.customer.email)
            # отправляем им письмо
            send_mails(serial, customers_emails)
