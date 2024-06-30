from django.contrib.auth.models import User
from django.db import models


class NewsQuote(models.Model):
    quote = models.TextField(verbose_name="Quote")
    author = models.CharField(max_length=250, verbose_name="Author")
    tags = models.CharField(max_length=250, verbose_name="Tags")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.quote}"


class NewsEconomics(models.Model):
    time = models.CharField(max_length=50, verbose_name="Time")
    text = models.CharField(max_length=250, verbose_name="Text")
    url = models.CharField(max_length=250, verbose_name="URL")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.text}"


class NewsPolitics(models.Model):
    time = models.CharField(max_length=50, verbose_name="Time")
    text = models.CharField(max_length=250, verbose_name="Text")
    url = models.CharField(max_length=250, verbose_name="URL")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.text}"


class NewsWeather(models.Model):
    day = models.CharField(max_length=50, verbose_name="Day")
    month = models.CharField(max_length=50, verbose_name="Month")
    degree = models.CharField(max_length=50, verbose_name="Degree")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.degree}"


class NewsWeatherByCity(models.Model):
    url = models.CharField(max_length=250, verbose_name="URL")
    city = models.CharField(max_length=100, verbose_name="City")
    degree = models.CharField(max_length=50, verbose_name="Degree")
    cloudy = models.CharField(max_length=100, verbose_name="Cloudy")
    humidity = models.CharField(max_length=20, verbose_name="Humidity")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.city} {self.degree} {self.cloudy} {self.humidity}"


class NewsUpdateTime(models.Model):
    news_type = models.CharField(max_length=250, verbose_name="News Type")
    update_time = models.DateTimeField(verbose_name="Creation Time")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.news_type} {self.update_time}"
