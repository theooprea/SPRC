from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Temperature
from .serializers import TemperatureSerializer
from datetime import datetime

# Time format, as specified in the assignment, year - month - day
TIME_FORMAT = "%Y-%m-%d"

class TemperaturesView(APIView):
    '''
    The view for all Temperatures in the database, handles a GET method
    which returns all Temperatures in the DB and a POST method, used to
    add a new temperature to the DB
    '''
    def get(self, request):
        # Prepare to build the query parameters, depending on the parameters
        # received in the request
        query_params = {}

        # Get the Query Params of the GET request
        params = {
            "lat": request.GET.get("lat", None),
            "lon": request.GET.get("lon", None),
            "from": request.GET.get("from", None),
            "until": request.GET.get("until", None),
        }

        # Update the query parameters (used to extract DB data) according to the
        # HTTP lat and lon Query Params
        if params["lat"] is not None:
            query_params.update({"id_oras__latitudine": params.get("lat", None)})
        if params["lon"] is not None:
            query_params.update({"id_oras__longitudine": params.get("lon", None)})
        
        # Update the query parameters (used to extract DB data) according to the
        # HTTP from and until Query Params
        if params["from"] is not None and params["until"] is not None:
            # Format the received dates in the TIME_FORMAT format and set the
            # min search time to the 00.00.00 time of the "from" day and set the
            # max search time to the 23.59.59 time of the "until" day
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__range": (datetime_from, datetime_until)})
        elif params["from"] is not None:
            # Format the received date in the TIME_FORMAT format and set the
            # min search time to the 00.00.00 time of that day
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            query_params.update({"timestamp__gte": datetime_from})
        elif params["until"] is not None:
            # Format the received date in the TIME_FORMAT format and set the
            # max search time to the 23.59.59 time of that day
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__lte": datetime_until})

        # Get all temperatures filtered by the built query and serialize the data
        temperatures = Temperature.objects.filter(**query_params)
        serializer = TemperatureSerializer(temperatures, many=True)

        # Return the data and a 200 Response Code
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        Adds a temperature to the DB
        '''
        # Format the payload data to DB format
        payload = {
            "id_oras": request.data.get("idOras", None),
            "valoare": request.data.get("valoare", None),
            "timestamp": None,
        }

        # Validate data and save it in the DB
        serializer = TemperatureSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            # Return the id of the newly created temperature and return 201 response code
            return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_201_CREATED)
        
        # In case of error, return the serializer error and 400 response code
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemperaturesPerCityView(APIView):
    '''
    The view for all Temperatures under a City in the database, handles a
    GET method returns all Temperatures under the given City, query by id
    '''
    def get(self, request, id_oras):
        # Prepare to build the query parameters, depending on the parameters
        # received in the request, first filter by city
        query_params = {"id_oras": id_oras}

        # Get the Query Params of the GET request
        params = {
            "from": request.GET.get("from", None),
            "until": request.GET.get("until", None),
        }

        # Update the query parameters (used to extract DB data) according to the
        # HTTP from and until Query Params
        if params["from"] is not None and params["until"] is not None:
            # Format the received dates in the TIME_FORMAT format and set the
            # min search time to the 00.00.00 time of the "from" day and set the
            # max search time to the 23.59.59 time of the "until" day
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__range": (datetime_from, datetime_until)})
        elif params["from"] is not None:
            # Format the received date in the TIME_FORMAT format and set the
            # min search time to the 00.00.00 time of that day
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            query_params.update({"timestamp__gte": datetime_from})
        elif params["until"] is not None:
            # Format the received date in the TIME_FORMAT format and set the
            # max search time to the 23.59.59 time of that day
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__lte": datetime_until})

        # Get all temperatures filtered by the built query and serialize the data
        temperatures = Temperature.objects.filter(**query_params)
        serializer = TemperatureSerializer(temperatures, many=True)

        # Return the data and a 200 Response Code
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class TemperaturesPerCountryView(APIView):
    '''
    The view for all Temperatures under a Country in the database, handles a
    GET method returns all Temperatures under the given Country, query by id
    '''
    def get(self, request, id_tara):
        # Prepare to build the query parameters, depending on the parameters
        # received in the request, first filter by country
        query_params = {"id_oras__id_tara": id_tara}

        # Get the Query Params of the GET request
        params = {
            "from": request.GET.get("from", None),
            "until": request.GET.get("until", None),
        }

        # Update the query parameters (used to extract DB data) according to the
        # HTTP from and until Query Params
        if params["from"] is not None and params["until"] is not None:
            # Format the received dates in the TIME_FORMAT format and set the
            # min search time to the 00.00.00 time of the "from" day and set the
            # max search time to the 23.59.59 time of the "until" day
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__range": (datetime_from, datetime_until)})
        elif params["from"] is not None:
            # Format the received date in the TIME_FORMAT format and set the
            # min search time to the 00.00.00 time of that day
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            query_params.update({"timestamp__gte": datetime_from})
        elif params["until"] is not None:
            # Format the received date in the TIME_FORMAT format and set the
            # max search time to the 23.59.59 time of that day
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__lte": datetime_until})

        # Get all temperatures filtered by the built query and serialize the data
        temperatures = Temperature.objects.filter(**query_params)
        serializer = TemperatureSerializer(temperatures, many=True)

        # Return the data and a 200 Response Code
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class TemperatureView(APIView):
    '''
    The view for a single Temperature in the database, handles a PUT method
    which updates a Temperature in the DB and a DELETE method, used to
    delete a temperature from the DB
    '''
    def put(self, request, pk):
        '''
        Updates a given temperature in the DB
        '''
        try:
            # Gets the temperature from the DB by the given id
            temperature = Temperature.objects.get(pk=pk)

            # Format the payload data to DB format
            payload = {
                "id": request.data.get("id", None),
                "id_oras": request.data.get("idOras", None),
                "valoare": request.data.get("valoare", None),
                "timestamp": temperature.timestamp,
            }

            # Checks for id validity
            if len(Temperature.objects.filter(pk=int(payload["id"]))) != 0 and payload["id"] != int(pk):
                return Response({"error": "conflict"}, status=status.HTTP_409_CONFLICT)

            # Validate data and save it in the DB
            serializer = TemperatureSerializer(temperature, data=payload)
            if serializer.is_valid():
                # Delete old entry and insert the new one
                temperature.delete()
                serializer.save()
                # Return the data of the updated temperature and return 200 response code
                return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_200_OK)
            
            # In case of error, return the serializer error and 400 response code
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # In case of not found, return the error data and 404 response code
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        '''
        Deletes a given Temperature from the DB
        '''
        try:
            # Get the given temperature and delete it
            temperature = Temperature.objects.get(pk=pk)
            temperature.delete()
            # Return the 'success' 200 response code
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            # In case of error, return the error data and 400 response code
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
