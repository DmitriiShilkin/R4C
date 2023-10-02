# импорт стандартной модели джанго
from django.db import models

# импорт валидаторов
from .validators import validate_model, validate_version, validate_serial


# модель робота
class Robot(models.Model):
    # поля модели, поле id создается автоматически
    serial = models.CharField(max_length=5, blank=False, null=False, validators=[validate_serial])
    model = models.CharField(max_length=2, blank=False, null=False, validators=[validate_model])
    version = models.CharField(max_length=2, blank=False, null=False, validators=[validate_version])
    created = models.DateTimeField(blank=False, null=False)

    # для понятного отображения объектов модели в админке
    def __str__(self):
        return self.serial
