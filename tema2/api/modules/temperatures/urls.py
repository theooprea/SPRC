from django.urls import path, re_path
from .views import TemperaturesView, TemperaturesPerCityView, TemperaturesPerCountryView,TemperatureView

app_name = 'temperatures'

urlpatterns = [
    # Route for the GET and POST methods
    path('', TemperaturesView.as_view(), name='temperaturesView'),
    # Route for the Get Temperatures per City method
    re_path('cities/(?P<id_oras>[0-9]+)', TemperaturesPerCityView.as_view(), name='temperaturesPerCityView'),
    # Route for the Get Temperatures per Country method
    re_path('countries/(?P<id_tara>[0-9]+)', TemperaturesPerCountryView.as_view(), name='temperaturesPerCountryView'),
    # Route for the PUT and DELETE methods
    re_path('(?P<pk>[0-9]+)', TemperatureView.as_view(), name='temperatureView'),
]
