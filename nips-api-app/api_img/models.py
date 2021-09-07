from django.db import models
from django.contrib.auth.models import User

from main.settings import MEDIA_ROOT
from api_img.image_transform import create_small_img

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from main.settings import FILE_MAX_SIZE


def validate_file_image_max_size(image):
    """
    Валидатор, для проверки размера изображение, не более 2 MB
    """
    if image.size > FILE_MAX_SIZE:
        raise ValidationError('Файл слишком большой, размер должен быть не больше 2 MB')


class Images(models.Model):
    BIG_IMG_PATH = "images/api_img/big/"
    SMALL_IMG_PATH = "images/api_img/min/"

    """Модель для CRUD операций с изображениями"""
    owner = models.ForeignKey(User, default=True, null=True, on_delete=models.SET_NULL, verbose_name='Владелец')
    type = models.CharField(max_length=255, verbose_name='Тип изображения')
    big_image = models.ImageField(upload_to=BIG_IMG_PATH, verbose_name='Большое изображение',
                              validators=[
                                  FileExtensionValidator(
                                      allowed_extensions=['jpg', 'jpeg'],
                                      message='Файл должен быть одним из: jpg, jpeg',
                                  ),
                                  validate_file_image_max_size,
                              ])
    min_image = models.ImageField(upload_to=SMALL_IMG_PATH, null=True, blank=True, verbose_name='Маленькое изображение')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    def __str__(self):
        return f'Id {self.id}:  {self.type}'

    def get_id(self):
        return self.id

    def get_owner(self):
        return self.owner

    def save(self, *args, **kwargs):
        """Сохраняем модель, генерируем минифицированнцю версию изображения"""
        super().save(*args, **kwargs)
        create_small_img(self, 500)
        super().save()

    def get_path_to_small_photo(self):
        """Путь к директории минифицированной версии картинки"""
        return "{0}/{1}".format(MEDIA_ROOT, self.SMALL_IMG_PATH)
