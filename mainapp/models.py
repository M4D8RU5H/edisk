import os
from django.db import models
from myproj import settings
from accounts.models import User

class file_upload(models.Model):
    ids = models.AutoField(primary_key=True)
    my_file = models.FileField(upload_to='')

    def __str__(self):
        return self.my_file


class FileModel(models.Model):
    ids = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', default=1)
    file = models.FileField(upload_to='')
