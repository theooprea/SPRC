from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country
from ..cities.models import City
from .serializers import CountrySerializer
from rest_framework import status
    
class CountriesView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        
        response_data = [{
            "id": country_data["id"],
            "nume": country_data["nume_tara"],
            "lat": country_data["latitudine"],
            "lon": country_data["longitudine"],
        } for country_data in serializer.data]
        
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        payload = {
            "nume_tara": request.data.get("nume", None),
            "latitudine": request.data.get("lat", None),
            "longitudine": request.data.get("lon", None),
        }
        
        serializer = CountrySerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountryView(APIView):
    def put(self, request, pk):
        try:
            country = Country.objects.get(pk=pk)
            print(country)
            payload = {
                "id": request.data.get("id", None),
                "nume_tara": request.data.get("nume", None),
                "latitudine": request.data.get("lat", None),
                "longitudine": request.data.get("lon", None),
            }

            if len(Country.objects.filter(pk=int(payload["id"]))) != 0 and payload["id"] != int(pk):
                return Response({"error": "conflict"}, status=status.HTTP_409_CONFLICT)

            serializer = CountrySerializer(country, data=payload)
            if serializer.is_valid():
                country.delete()
                serializer.save()
                City.objects.filter(id_tara=pk).update(id_tara=payload["id"])
                return Response(serializer.data)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            country = Country.objects.get(pk=pk)
            country.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
