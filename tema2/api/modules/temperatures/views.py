from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Temperature
from .serializers import TemperatureSerializer

class HomeView(APIView):
    def get(self, request):
        return Response(data={"data": "salut"})

class TemperaturesView(APIView):
    def get(self, request):
        temperatures = Temperature.objects.all()
        serializer = TemperatureSerializer(temperatures, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
