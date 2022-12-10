from rest_framework import serializers
from .models import Country

# Serializer for the Country model, used to validate data received
# from the API and to serialize the data from the DB to be served
# to GET methods
class CountrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = ['id', 'nume_tara', 'latitudine', 'longitudine']
