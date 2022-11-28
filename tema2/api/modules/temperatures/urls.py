from django.urls import path, re_path
from .views import TemperaturesView, TemperaturesPerCityView, TemperaturesPerCountryView,TemperatureView

app_name = 'temperatures'

urlpatterns = [
    path('', TemperaturesView.as_view(), name='temperaturesView'),
    re_path('cities/(?P<id_oras>[0-9]+)', TemperaturesPerCityView.as_view(), name='temperaturesPerCityView'),
    re_path('countries/(?P<id_tara>[0-9]+)', TemperaturesPerCountryView.as_view(), name='temperaturesPerCountryView'),
    re_path('(?P<pk>[0-9]+)', TemperatureView.as_view(), name='temperatureView'),
]
