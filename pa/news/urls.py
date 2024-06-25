from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.main, name="main"),
    path("quotes/get", views.quotes_get, name="quotes_get"),
    path("economics/", views.economics, name="economics"),
    path("economics/get", views.economics_get, name="economics_get"),
    path("politics/", views.politics, name="politics"),
    path("politics/get", views.politics_get, name="politics_get"),
    path("weather_forecast/", views.weather_forecast, name="weather_forecast"),
    path(
        "weather_forecast/get", views.weather_forecast_get, name="weather_forecast_get"
    ),
]
