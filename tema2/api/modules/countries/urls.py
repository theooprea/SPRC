from django.urls import path
from .views import CountriesView, CountryView

app_name = 'countries'

urlpatterns = [
    path('', CountriesView.as_view(), name='countriesview'),
    path('<int:pk>/', CountryView.as_view(), name='countryview')
]
