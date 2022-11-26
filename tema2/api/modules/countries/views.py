from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer
from rest_framework import status
    
class CountriesView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        
        serializer = CountrySerializer(countries, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        payload = {
            "nume_tara": request.data.get("nume", None),
            "latitudine": request.data.get("lat", None),
            "longitudine": request.data.get("lon", None),
        }
        
        serializer = CountrySerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountryView(APIView):
    def put(self, request, pk):
        try:
            country = Country.objects.get(pk=pk)
            payload = {
                "nume_tara": request.data.get("nume", None),
                "latitudine": request.data.get("lat", None),
                "longitudine": request.data.get("lon", None),
            }

            serializer = CountrySerializer(country, data=payload)
            if serializer.is_valid():
                serializer.save()
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
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
