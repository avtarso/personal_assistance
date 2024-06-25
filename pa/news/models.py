from django.contrib.auth.models import User
from django.db import models


# class NewsQuote(models.Model):
#     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class NewsQuote(models.Model):
    quote = models.TextField(null=False, unique=True, verbose_name="Quote")
    author = models.CharField(max_length=250, verbose_name="Author")
    tags = models.CharField(max_length=250, verbose_name="Tags")
    ctime = models.DateTimeField(
        null=False, auto_now_add=True, verbose_name="Creation Time"
    )

    def __str__(self):
        return f"{self.quote}"


class NewsEconomics(models.Model):
    time = models.CharField(max_length=50, verbose_name="Time")
    text = models.CharField(max_length=250, verbose_name="Text")
    url = models.CharField(max_length=250, verbose_name="URL")

    def __str__(self):
        return f"{self.text}"


class NewsPolitics(models.Model):
    time = models.CharField(max_length=50, verbose_name="Time")
    text = models.CharField(max_length=250, verbose_name="Text")
    url = models.CharField(max_length=250, verbose_name="URL")

    def __str__(self):
        return f"{self.text}"
