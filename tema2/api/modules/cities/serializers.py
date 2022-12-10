from rest_framework import serializers
from .models import City

# Serializer for the City model, used to validate data received
# from the API and to serialize the data from the DB to be served
# to GET methods
class CitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = City
        fields = ['id', 'id_tara', 'nume_oras', 'latitudine', 'longitudine']
