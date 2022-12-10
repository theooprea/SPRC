from django.urls import re_path, path
from .views import CountriesView, CountryView

app_name = 'countries'

urlpatterns = [
    # Route for the GET and POST methods
    path('', CountriesView.as_view(), name='countriesView'),
    # Route for the PUT and DELETE methods
    re_path('(?P<pk>[0-9]+)/?$', CountryView.as_view(), name='countryView'),
]
