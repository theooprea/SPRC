from rest_framework import serializers
from .models import Temperature

TIME_FORMAT = "%Y-%m-%d"

class TemperatureSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format=TIME_FORMAT)
    class Meta:
        model = Temperature
        fields = ['id', 'valoare', 'timestamp', 'id_oras']
