# импорт исключения при ошибках валидации
from django.core.exceptions import ValidationError

# список существующих серийных номеров, кортежи нужны для выбора значений из выпадающего списка в форме создания заказа
SERIALS = [
    ('R2-A1', 'R2-A1'),
    ('R2-D2', 'R2-D2'),
    ('R2-C8', 'R2-C8'),
    ('13-XS', '13-XS'),
    ('X5-LT', 'X5-LT'),
]

# список существующих моделей роботов
MODELS = list({i[0][:2] for i in SERIALS})

# список существующих версий роботов
VERSIONS = list({j[0][-2:] for j in SERIALS})


# валидатор моделей роботов
def validate_model(value):
    # если введенное значение отсутствует в списке
    if value not in MODELS:
        raise ValidationError(
            f'{value} не соответствует существующим моделям роботов.',
            params={'value': value},
        )


# валидатор версий роботов
def validate_version(value):
    # если введенное значение отсутствует в списке
    if value not in VERSIONS:
        raise ValidationError(
            f'{value} не соответствует существующим версиям роботов.',
            params={'value': value},
        )


# валидатор серийных номеров роботов
def validate_serial(value):
    # преобразуем список кортежей в список значений
    serials = [ser[0] for ser in SERIALS]
    # если введенное значение отсутствует в списке
    if value not in serials:
        raise ValidationError(
            f'Модель-Версия {value} не существует! Укажите другую модель или версию.',
            params={'value': value},
        )
