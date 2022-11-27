from rest_framework import serializers
from .models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'id_tara', 'nume_oras', 'latitudine', 'longitudine']
