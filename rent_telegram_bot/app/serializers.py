
from rest_framework import serializers

from .models import Moto, Yacht


class MotoSerializer(serializers.ModelSerializer):
    """"
    Moto Сериализатор
    """

    class Meta:
        model = Moto
        fields = '__all__'


class YachtSerializer(serializers.ModelSerializer):
    """"
    Moto Сериализатор
    """

    class Meta:
        model = Yacht
        fields = '__all__'
