from rest_framework.viewsets import ModelViewSet
from .serializers import ImagesSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Images

# Права доступа
from . import custom_permissions
from rest_framework import permissions


# Импорт модулей для поиска, фильтрации и сортировки для API
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Модули для стилизации изображений
from image_transform.img_stylize import stylize_images
from image_transform.neural_stylize import neural_style_transfer


class ImagesViewSet(ModelViewSet):
    """Все CRUD к модели Images"""
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['id', 'type']
    ordering_fields = ['id', 'type']
    # permission_classes = {custom_permissions.IsOwnerOrStaffOrReadOnly}
    permission_classes = {permissions.AllowAny}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_data = {}

    def create(self, request, *args, **kwargs):
        """
        Переопределенный метод сохранения записи, или
        создание комбинированной картинки на основе JSON

        1) Создать запись: POST host/api/v1/images/
        2) пример JSON для создания изображения.
        { "bind_images": {"photo_id": 3, "filter_id": 8} }
        """
        if self.validate_request(request.data) and self.validate_objects(request.data):
            # Выбираем одну из функций создания изображения
            stylize_img = stylize_images(
                image=self.custom_data['photo'].big_image.path,
                filter=self.custom_data['filter'].big_image.path,
                alpha_value=128
            )
            # stylize_img = neural_style_transfer(
            #     img_photo=self.custom_data['photo'].big_image.path,
            #     img_style=self.custom_data['filter'].big_image.path,
            #     quality=20
            # )

            # Создаем обьект и сохраняем его
            new_image = Images(type='result', big_image=Images.BIG_IMG_PATH + stylize_img)
            new_image.save()

            # Отдаем ответ, о создании нового стилизованного изображения
            response = {
                "message": "Successfully created",
                "id": new_image.get_id(),
            }
            return Response(response, status=status.HTTP_201_CREATED)

        # POST стандартный процесс на создание записи
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            "status": status.HTTP_201_CREATED,
            "message": "Successfully created",
            "id": serializer.instance.get_id(),
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def validate_request(self, data):
        """Проверка, есть ли в JSON нужные параметры."""
        if "bind_images" in data \
                and "photo_id" in data["bind_images"] \
                and "filter_id" in data["bind_images"] \
                and isinstance(data["bind_images"]["photo_id"], int) and \
                isinstance(data["bind_images"]["filter_id"], int):
            return True

    def validate_objects(self, data):
        """Проверка обьектов на существование."""
        try:
            photo = Images.objects.get(pk=data["bind_images"]["photo_id"])
            filter = Images.objects.get(pk=data["bind_images"]["filter_id"])
            if photo.type != "photo" and filter.type != "filter":
                raise Exception
        except Exception:
            return False

        self.custom_data['photo'] = photo
        self.custom_data['filter'] = filter
        return True

    # TODO стоит ли кидать ошибку если текущий пользователь
    #  пытается сохранить запись не под собой ? сейчас просто
    #  ничего не делаем, даже предупреждений
    # TODO если спер юзер или админ не указали кто является
    #  владельцем, то так оно и будет, поле будет null
    def perform_create(self, serializer):
        """
        Переопределяем метод сохранения модели из сериализатора.

        Если пользователь супер или админ, то сохраняем, если он не
        супер и не админ, то сохраняем запись под текущим пользователем.
        """
        # if not self.request.user.is_superuser and not self.request.user.is_staff:
        #     serializer.validated_data['owner'] = self.request.user
        # serializer.save()
        serializer.save()

    # TODO стоит ли кидать тут ошибку, если пользователь
    #  пытается отредактировать не свою запись ? сейчас просто
    #  ничего не делаем, даже предупреждений
    def perform_update(self, serializer):
        """
        Переопределяем метод обновления модели из сериализатора.

        Если пользователь супер или админ, то сохраняем изменения,сли
        пользователь не супер и не админ но владелец записи, то
        сохраняем изменения в записи под текущим пользователем.
        """
        # if (self.request.user.is_superuser or self.request.user.is_staff) or\
        #         (serializer.validated_data['owner'] == serializer.instance.get_owner()):
        #     serializer.save()
        serializer.save()
