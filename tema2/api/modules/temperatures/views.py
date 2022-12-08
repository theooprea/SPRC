from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Temperature
from .serializers import TemperatureSerializer
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d"

class TemperaturesView(APIView):
    def get(self, request):
        query_params = {}
        params = {
            "lat": request.GET.get("lat", None),
            "lon": request.GET.get("lon", None),
            "from": request.GET.get("from", None),
            "until": request.GET.get("until", None),
        }

        if params["lat"] is not None:
            query_params.update({"id_oras__latitudine": params.get("lat", None)})
        if params["lon"] is not None:
            query_params.update({"id_oras__longitudine": params.get("lon", None)})
        
        if params["from"] is not None and params["until"] is not None:
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__range": (datetime_from, datetime_until)})
        elif params["from"] is not None:
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            query_params.update({"timestamp__gte": datetime_from})
        elif params["until"] is not None:
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__lte": datetime_until})

        temperatures = Temperature.objects.filter(**query_params)

        serializer = TemperatureSerializer(temperatures, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        payload = {
            "id_oras": request.data.get("idOras", None),
            "valoare": request.data.get("valoare", None),
            "timestamp": None,
        }

        serializer = TemperatureSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemperaturesPerCityView(APIView):
    def get(self, request, id_oras):
        query_params = {"id_oras": id_oras}
        params = {
            "from": request.GET.get("from", None),
            "until": request.GET.get("until", None),
        }

        if params["from"] is not None and params["until"] is not None:
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__range": (datetime_from, datetime_until)})
        elif params["from"] is not None:
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            query_params.update({"timestamp__gte": datetime_from})
        elif params["until"] is not None:
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__lte": datetime_until})

        temperatures = Temperature.objects.filter(**query_params)

        serializer = TemperatureSerializer(temperatures, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class TemperaturesPerCountryView(APIView):
    def get(self, request, id_tara):
        query_params = {"id_oras__id_tara": id_tara}
        params = {
            "from": request.GET.get("from", None),
            "until": request.GET.get("until", None),
        }

        if params["from"] is not None and params["until"] is not None:
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__range": (datetime_from, datetime_until)})
        elif params["from"] is not None:
            datetime_from = datetime.strptime(params["from"], TIME_FORMAT)
            query_params.update({"timestamp__gte": datetime_from})
        elif params["until"] is not None:
            datetime_until = datetime.combine(
                datetime.strptime(params["until"], TIME_FORMAT),
                datetime.strptime(params["until"], TIME_FORMAT).time().max
            )
            query_params.update({"timestamp__lte": datetime_until})

        temperatures = Temperature.objects.filter(**query_params)

        serializer = TemperatureSerializer(temperatures, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class TemperatureView(APIView):
    def put(self, request, pk):
        try:
            temperature = Temperature.objects.get(pk=pk)
            payload = {
                "id": request.data.get("id", None),
                "id_oras": request.data.get("idOras", None),
                "valoare": request.data.get("valoare", None),
                "timestamp": temperature.timestamp,
            }

            if len(Temperature.objects.filter(pk=int(payload["id"]))) != 0 and payload["id"] != int(pk):
                return Response({"error": "conflict"}, status=status.HTTP_409_CONFLICT)

            serializer = TemperatureSerializer(temperature, data=payload)
            if serializer.is_valid():
                temperature.delete()
                serializer.save()
                return Response(data={"id": serializer.data.get("id", None)}, status=status.HTTP_200_OK)
            
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            temperature = Temperature.objects.get(pk=pk)
            temperature.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
