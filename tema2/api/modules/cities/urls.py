from django.urls import path, re_path
from .views import CitiesView, CitiesPerCountryView, CityView

app_name = 'cities'

urlpatterns = [
    # Route for the GET and POST methods
    path('', CitiesView.as_view(), name='citiesView'),
    # Route for the Get City per Country method
    re_path('country/(?P<id_Tara>[0-9]+)/?$', CitiesPerCountryView.as_view(), name='citiesPerCountryView'),
    # Route for the PUT and DELETE methods
    re_path('(?P<pk>[0-9]+)/?$', CityView.as_view(), name='cityView'),
]
