from django.urls import path, re_path
from .views import TemperaturesView

app_name = 'temperatures'

urlpatterns = [
    path('', TemperaturesView.as_view(), name='temperaturesView')
]
