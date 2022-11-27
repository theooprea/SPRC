from django.urls import re_path, path
from .views import CountriesView, CountryView

app_name = 'countries'

urlpatterns = [
    path('', CountriesView.as_view(), name='countriesview'),
    re_path('(?P<pk>[0-9]+)/?$', CountryView.as_view(), name='countryview'),
]
