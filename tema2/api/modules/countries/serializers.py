from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = ['id', 'nume_tara', 'latitudine', 'longitudine']
