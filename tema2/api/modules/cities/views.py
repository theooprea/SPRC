from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import City
from .serializers import CitySerializer
from ..temperatures.models import Temperature
    
class CitiesView(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)

        response_data = [{
            "id": city_data["id"],
            "idTara": city_data["id_tara"],
            "nume": city_data["nume_oras"],
            "lat": city_data["latitudine"],
            "lon": city_data["longitudine"],
        } for city_data in serializer.data]
        
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        payload = {
            "id_tara": request.data.get("idTara", None),
            "nume_oras": request.data.get("nume", None),
            "latitudine": request.data.get("lat", None),
            "longitudine": request.data.get("lon", None),
        }

        serializer = CitySerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CitiesPerCountryView(APIView):
    def get(self, request, id_Tara):
        try:
            cities = City.objects.filter(id_tara=id_Tara)
            serializer = CitySerializer(cities, many=True)

            response_data = [{
                "id": city_data["id"],
                "idTara": city_data["id_tara"],
                "nume": city_data["nume_oras"],
                "lat": city_data["latitudine"],
                "lon": city_data["longitudine"],
            } for city_data in serializer.data]
            
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CityView(APIView):
    def put(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            payload = {
                "id": request.data.get("id", None),
                "id_tara": request.data.get("idTara", None),
                "nume_oras": request.data.get("nume", None),
                "latitudine": request.data.get("lat", None),
                "longitudine": request.data.get("lon", None),
            }

            serializer = CitySerializer(city, data=payload)
            if serializer.is_valid():
                city.delete()
                serializer.save()
                Temperature.objects.filter(id_oras=pk).update(id_oras=payload["id"])
                return Response(serializer.data)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            city = City.objects.get(pk=pk)
            city.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
