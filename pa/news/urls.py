from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.main, name="main"),
    path("quotes/", views.main, name="main"),
    path("quotes/get", views.quotes_get, name="quotes_get"),
    path("economics/", views.economics, name="economics"),
    path("economics/get", views.economics_get, name="economics_get"),
    path("politics/", views.politics, name="politics"),
    path("politics/get", views.politics_get, name="politics_get"),
    path("weather/", views.weather, name="weather"),
    path("weather/get", views.weather_get, name="weather_get"),
]
