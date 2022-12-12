from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country
from ..cities.models import City
from ..temperatures.models import Temperature
from .serializers import CountrySerializer
from rest_framework import status

class CountriesView(APIView):
    '''
    The view for all Countries in the database, handles a GET method
    which returns all Countries in the DB and a POST method, used to
    add a new country to the DB
    '''
    def get(self, request):
        '''
        Returns all countries in the DB
        '''
        # Retrieve all countries from the database and serialize all the objects
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)

        # Format the DB data to the as-requested-in-the-assignment format 
        response_data = [{
            "id": country_data["id"],
            "nume": country_data["nume_tara"],
            "lat": country_data["latitudine"],
            "lon": country_data["longitudine"],
        } for country_data in serializer.data]

        # Return the data and a 200 Response Code
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        Adds a country to the DB
        '''
        # Format the payload data to DB format
        payload = {
            "nume_tara": request.data.get("nume", None),
            "latitudine": request.data.get("lat", None),
            "longitudine": request.data.get("lon", None),
        }

        # Validate data and save it in the DB
        serializer = CountrySerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            # Return the id of the newly created country and return 201 response code
            return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_201_CREATED)
        
        # In case of error, return the serializer error and 400 response code
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountryView(APIView):
    '''
    The view for a single Country in the database, handles a PUT method
    which updates a Country in the DB and a DELETE method, used to
    delete a country from the DB
    '''
    def put(self, request, pk):
        '''
        Updates a given country in the DB
        '''
        try:
            # Gets the country from the DB by the given id
            country = Country.objects.get(pk=pk)

            # Format the payload data to DB format
            payload = {
                "id": request.data.get("id", None),
                "nume_tara": request.data.get("nume", None),
                "latitudine": request.data.get("lat", None),
                "longitudine": request.data.get("lon", None),
            }

            # Checks for id validity
            if len(Country.objects.filter(pk=int(payload["id"]))) != 0 and payload["id"] != int(pk):
                return Response({"error": "conflict"}, status=status.HTTP_409_CONFLICT)

            # Validate data and save it in the DB
            serializer = CountrySerializer(country, data=payload)
            if serializer.is_valid():
                # Delete old entry and insert the new one
                country.delete()
                serializer.save()
                # Update all cities that are in the given country to the newly updated id
                City.objects.filter(id_tara=pk).update(id_tara=payload["id"])
                # Return the data of the updated country and return 200 response code
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            # In case of error, return the serializer error and 400 response code
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # In case of not found, return the error data and 404 response code
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        '''
        Deletes a given Country from the DB, with all of its Cities and Temperatures data
        '''
        try:
            # Get the given country from the DB, as well as all of its cities and temperatures
            country = Country.objects.get(pk=pk)
            cities = City.objects.filter(id_tara=country.id)
            temperatures = Temperature.objects.filter(id_oras__in=cities.values_list("id", flat=True))
            # Delete in cascade
            temperatures.delete()
            cities.delete()
            country.delete()
            # Return the 'success' 200 response code
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            # In case of error, return the error data and 400 response code
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
