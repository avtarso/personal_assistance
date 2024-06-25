from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Note(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.description}, {self.tags}"
