from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=30, null=False)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=50, null=True)
    birthday = models.DateField(null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (f"{self.name}, {self.address},"
                f"{self.phone}, {self.email},"
                f"{self.birthday}")
