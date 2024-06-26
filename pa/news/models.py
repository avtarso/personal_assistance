from django.contrib.auth.models import User
from django.db import models


class NewsQuote(models.Model):
    quote = models.TextField(verbose_name="Quote")
    author = models.CharField(max_length=250, verbose_name="Author")
    tags = models.CharField(max_length=250, verbose_name="Tags")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quote}"


class NewsEconomics(models.Model):
    time = models.CharField(max_length=50, verbose_name="Time")
    text = models.CharField(max_length=250, verbose_name="Text")
    url = models.CharField(max_length=250, verbose_name="URL")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"


class NewsPolitics(models.Model):
    time = models.CharField(max_length=50, verbose_name="Time")
    text = models.CharField(max_length=250, verbose_name="Text")
    url = models.CharField(max_length=250, verbose_name="URL")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"


class NewsWeather(models.Model):
    day = models.CharField(max_length=50, verbose_name="Day")
    month = models.CharField(max_length=50, verbose_name="Month")
    degree = models.CharField(max_length=50, verbose_name="Degree")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.degree}"
