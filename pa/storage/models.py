# storage/models.py
from django.db import models
from django.contrib.auth.models import User


class FileTag(models.Model):
    name = models.CharField(max_length=50)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    upload_time = models.DateTimeField(auto_now_add=True)
    telegram_file_id = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    tg_message_id = models.PositiveIntegerField()
    attention_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField('FileTag', blank=True)
    description = models.TextField(blank=True, null=True)



