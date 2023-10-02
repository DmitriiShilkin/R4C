# импортируем найстройки для чтения констант из settings.py
from django.conf import settings

# импортируем инструменты для работы с электронной почтой
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# отправка письма на электронную почту
def send_mails(serial, customers_emails):
    # указываем какой шаблон и какие контекстные переменные брать за основу, преобразовываем их в строку для отправки
    # клиенту
    html_context = render_to_string(
        'robot_add_email.html',
        {
            'model': serial[:2],
            'version': serial[-2:],
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject='Робот в наличии',
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов, адресаты не будут отображаться в поле письма "Кому", позволяет не раскрывать персональные
        # данные клиентов при массовой рассылке
        bcc=customers_emails,
    )

    msg.attach_alternative(html_context, 'text/html')
    # отключаем вывод ошибки пользователю, если по какой-то причине отправка оказалась безуспешной
    msg.send(fail_silently=True)
