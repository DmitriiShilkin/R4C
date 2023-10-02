from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders'
    # подключение сигналов
    def ready(self):
        import orders.signals
