from rest_framework import serializers
from .models import Temperature

# Time format, as specified in the assignment, year - month - day
TIME_FORMAT = "%Y-%m-%d"

# Serializer for the Temperature model, used to validate data received
# from the API and to serialize the data from the DB to be served
# to GET methods
class TemperatureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    timestamp = serializers.DateTimeField(format=TIME_FORMAT, allow_null=True)

    class Meta:
        model = Temperature
        fields = ['id', 'valoare', 'timestamp', 'id_oras']
        # id_oras is write_only, since the assignment specifies the GET
        # methonds shouldn't return the city id of the temperature
        extra_kwargs = {
            'id_oras': {'write_only': True},
        }
