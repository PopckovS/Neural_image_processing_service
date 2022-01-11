from rest_framework.serializers import ModelSerializer

from .models import ImagesModel


class ImagesSerializer(ModelSerializer):
    """Сериализатор CRUD операций к модели Images"""
    class Meta:
        model = ImagesModel
        fields = ['id', 'type', 'big_image', 'min_image', 'parent_photo', 'parent_filter']
