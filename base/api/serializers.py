from rest_framework.serializers import ModelSerializer
from base.models import Space


class SpaceSerializer(ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'