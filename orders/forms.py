# импорт стандартных форм Джанго
from django import forms

# импорт виджетов
from django.forms import EmailInput, Select

# импорт моделей клиента и заказа, а также серийных номеров для выбора в выпадающем списке
from customers.models import Customer
from robots.validators import SERIALS
from .models import Order


# Форма отправки заказа на робота
class OrderForm(forms.ModelForm):
    # описание полей формы
    customer_email = forms.EmailField(
        widget=EmailInput(attrs={'type': 'email'}),
        max_length=255,
        label='E-mail',
        label_suffix='',
    )
    robot_serial = forms.ChoiceField(
        widget=Select,
        choices=SERIALS,
        label='Модель-Версия',
        label_suffix='',
    )

    class Meta:
        # используемая модель
        model = Order
        # поля, которые будут выводиться в форму, в порядке указания в списке
        fields = [
            'customer_email',
            'robot_serial',
        ]

    # для того, чтобы при создании заказа не возникала ошибка, нам нужно по введенному адресу электронной почты
    # найти в БД или создать нового клиента и привязать его к заказу
    def clean(self):
        cleaned_data = super().clean()
        # получаем введенный адрес эл. почты
        customer_email = cleaned_data.get('customer_email')
        # отфильтровываем всех клиентов с таким адресом
        customer = Customer.objects.filter(email=customer_email)
        # если такой клиент есть в кверисете
        if customer.exists():
            # берем первого
            customer = customer.first()
        else:
            # если нет, создаем нового
            customer = Customer.objects.create(email=customer_email)
        # присваиваем заказу полученного клиента
        self.instance.customer = customer
        return cleaned_data
