from rest_framework.serializers import ModelSerializer

from animals.models import Animal


class AnimalSerializer(ModelSerializer):
    class Meta:
        model = Animal
        fields = ('id', 'name')