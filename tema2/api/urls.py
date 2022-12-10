"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

app_name = 'tema2'

# The main app router, routes the requests to each view, the Country, City and Temperature Views
urlpatterns = [
    # Route to the admin views
    path('admin/', admin.site.urls),
    # Route to the Country View
    re_path(r'^api/countries/?', include('api.modules.countries.urls', namespace='countries')),
    # Route to the City View
    re_path(r'^api/cities/?', include('api.modules.cities.urls', namespace='cities')),
    # Route to the Temperature View
    re_path(r'^api/temperatures/?', include('api.modules.temperatures.urls', namespace='temperatures')),
]
