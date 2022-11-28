from rest_framework import serializers
from .models import Temperature

TIME_FORMAT = "%Y-%m-%d"

class TemperatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(format=TIME_FORMAT, allow_null=True)

    class Meta:
        model = Temperature
        fields = ['id', 'valoare', 'timestamp', 'id_oras']
        extra_kwargs = {
            'id_oras': {'write_only': True},
        }
