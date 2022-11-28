from rest_framework import serializers
from .models import City

class CitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = City
        fields = ['id', 'id_tara', 'nume_oras', 'latitudine', 'longitudine']
