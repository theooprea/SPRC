from django.urls import path, re_path
from .views import CitiesView, CitiesPerCountryView, CityView

app_name = 'cities'

urlpatterns = [
    path('', CitiesView.as_view(), name='citiesView'),
    re_path('country/(?P<id_Tara>[0-9]+)/?$', CitiesPerCountryView.as_view(), name='citiesPerCountryView'),
    re_path('(?P<pk>[0-9]+)/?$', CityView.as_view(), name='cityView'),
]
