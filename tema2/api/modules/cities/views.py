from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import City
from .serializers import CitySerializer
from ..temperatures.models import Temperature
    
class CitiesView(APIView):
    '''
    The view for all Cities in the database, handles a GET method
    which returns all Cities in the DB and a POST method, used to
    add a new city to the DB
    '''
    def get(self, request):
        '''
        Returns all cities in the DB
        '''
        # Retrieve all cities from the database and serialize all the objects
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)

        # Format the DB data to the as-requested-in-the-assignment format 
        response_data = [{
            "id": city_data["id"],
            "idTara": city_data["id_tara"],
            "nume": city_data["nume_oras"],
            "lat": city_data["latitudine"],
            "lon": city_data["longitudine"],
        } for city_data in serializer.data]

        # Return the data and a 200 Response Code
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        Adds a city to the DB
        '''
        # Format the payload data to DB format
        payload = {
            "id_tara": request.data.get("idTara", None),
            "nume_oras": request.data.get("nume", None),
            "latitudine": request.data.get("lat", None),
            "longitudine": request.data.get("lon", None),
        }

        # Validate data and save it in the DB
        serializer = CitySerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            # Return the id of the newly created city and return 201 response code
            return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_201_CREATED)

        # In case of error, return the serializer error and 400 response code
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CitiesPerCountryView(APIView):
    '''
    The view for all Cities under a Country in the database, handles a
    GET method returns all Cities under the given Country, query by id
    '''
    def get(self, request, id_Tara):
        try:
            # Get all cities under the given country
            cities = City.objects.filter(id_tara=id_Tara)

            # Serialize the data
            serializer = CitySerializer(cities, many=True)

            # Format the DB data to the as-requested-in-the-assignment format 
            response_data = [{
                "id": city_data["id"],
                "idTara": city_data["id_tara"],
                "nume": city_data["nume_oras"],
                "lat": city_data["latitudine"],
                "lon": city_data["longitudine"],
            } for city_data in serializer.data]

            # Return the data and a 200 Response Code
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # In case of error, return the serializer error and 400 response code
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CityView(APIView):
    '''
    The view for a single City in the database, handles a PUT method
    which updates a City in the DB and a DELETE method, used to
    delete a city from the DB
    '''
    def put(self, request, pk):
        '''
        Updates a given city in the DB
        '''
        try:
            # Gets the city from the DB by the given id
            city = City.objects.get(pk=pk)

            # Format the payload data to DB format
            payload = {
                "id": request.data.get("id", None),
                "id_tara": request.data.get("idTara", None),
                "nume_oras": request.data.get("nume", None),
                "latitudine": request.data.get("lat", None),
                "longitudine": request.data.get("lon", None),
            }

            # Checks for id validity
            if len(City.objects.filter(pk=int(payload["id"]))) != 0 and payload["id"] != int(pk):
                return Response({"error": "conflict"}, status=status.HTTP_409_CONFLICT)

            # Validate data and save it in the DB
            serializer = CitySerializer(city, data=payload)
            if serializer.is_valid():
                # Delete old entry and insert the new one
                city.delete()
                serializer.save()
                # Update all temperatures that are in the given city to the newly updated id
                Temperature.objects.filter(id_oras=pk).update(id_oras=payload["id"])
                # Return the data of the updated country and return 200 response code
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            # In case of error, return the serializer error and 400 response code
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # In case of error, return the error data and 400 response code
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        '''
        Deletes a given City from the DB, with all of its Temperatures data
        '''
        try:
            # Get the given city from the DB, as well as all of its temperatures
            city = City.objects.get(pk=pk)
            temperatures = Temperature.objects.filter(id_oras=city.id)
            # Delete in cascade
            temperatures.delete()
            city.delete()
            # Return the 'success' 200 response code
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            # In case of error, return the error data and 400 response code
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
