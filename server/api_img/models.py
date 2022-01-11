import os

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver


def validate_file_image_max_size(image):
    """Валидатор, проверки размера изображение, не более указанного в настройках"""
    if image.size > settings.FILE_MAX_SIZE:
        raise ValidationError('Файл слишком большой, размер должен быть не больше 2 MB')


class ImageType(models.TextChoices):
    """"""
    PHOTO = ('photo', 'photo')
    FILTER = ('filter', 'filter')
    RESULT = ('result', 'result')


class ImagesModel(models.Model):
    """Модель для изображений."""

    # Сообщение ошибки, для недопустимых форматов загружаемых изображений
    big_image_message_error = ', '.join(settings.UPLOAD_IMAGE)

    type = models.CharField(max_length=6, choices=ImageType.choices,
                            default=ImageType.PHOTO, verbose_name='Тип изображения'
                            )
    big_image = models.ImageField(upload_to=settings.BIG_IMG_PATH, blank=True,
                                  null=True, verbose_name='Большое изображение',
                                  validators=[
                                      FileExtensionValidator(
                                          allowed_extensions=settings.UPLOAD_IMAGE,
                                          message=f'Файл должен быть одним из: {big_image_message_error}'
                                      ),
                                      validate_file_image_max_size,
                                  ],
                                  )
    min_image = models.ImageField(upload_to=settings.SMALL_IMG_PATH, blank=True,
                                  null=True, verbose_name='Маленькое изображение'
                                  )
    parent_photo = models.ForeignKey('self', null=True, blank=True, related_name='+',
                                     on_delete=models.SET_NULL, verbose_name='Фото родитель'
                                     )
    parent_filter = models.ForeignKey('self', null=True, blank=True, related_name='+',
                                      on_delete=models.SET_NULL, verbose_name='Фильтр родитель'
                                      )

    def __str__(self):
        return f'Id {self.id}:  {self.type}'

    def get_path_to_small_photo(self):
        """Абсолютный путь к миниатюрной версии картинки"""
        return os.path.join(str(settings.MEDIA_ROOT), str(settings.SMALL_IMG_PATH))
        # return f"{settings.MEDIA_ROOT}/{settings.SMALL_IMG_PATH}"

    class Meta:
        db_table = 'nips_images'


def create_small_img(instance, size=500):
    """Создает миниатюрную версию изображения"""
    img = Image.open(instance.big_image.path)
    if img.height > size or img.width > size:
        img.thumbnail((size, size))
        img.save(instance.get_path_to_small_photo() + os.path.basename(instance.big_image.path))
        min_image_path = os.path.join(settings.SMALL_IMG_PATH, os.path.basename(instance.big_image.path))
    else:
        min_image_path = instance.big_image
    ImagesModel.objects.filter(pk=instance.pk).update(min_image=min_image_path)


@receiver(pre_save, sender=ImagesModel)
def on_change_pre_save(sender, instance, **kwargs):
    """Если изображения обновляются, а не создаются в первый раз, то удаляем старые изображения"""
    if instance.id is not None:
        previous = ImagesModel.objects.get(pk=instance.id)
        if previous.big_image.name != instance.big_image.name and os.path.isfile(previous.big_image.name):
            os.remove(previous.big_image.path)
        if previous.min_image.name != instance.min_image.name and os.path.isfile(previous.min_image.name):
            os.remove(previous.min_image.path)


@receiver(post_save, sender=ImagesModel)
def on_change_post_save(sender, instance, **kwargs):
    """Создаем миниатюрные версии изображений"""
    if instance.big_image and os.path.isfile(instance.big_image.path):
        create_small_img(instance, size=500)


@receiver(post_delete, sender=ImagesModel)
def on_delete_post(sender, instance, **kwargs):
    """Удаляем изображения привязанные к записи в модели."""
    if instance.big_image.name and os.path.isfile(instance.big_image.path):
        os.remove(instance.big_image.path)
    if instance.min_image.name and os.path.isfile(instance.min_image.path):
        os.remove(instance.min_image.path)

