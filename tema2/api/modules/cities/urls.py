from django.urls import path, re_path
from .views import CitiesView, CitiesPerCountryView, CityView

app_name = 'cities'

urlpatterns = [
    path('', CitiesView.as_view(), name='citiesview'),
    re_path('country/(?P<id_Tara>[0-9]+)/?$', CitiesPerCountryView.as_view(), name='citiespercountryview'),
    re_path('(?P<pk>[0-9]+)/?$', CityView.as_view(), name='cityview'),
]
