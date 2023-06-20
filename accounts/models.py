from myproj import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    storage_space = models.IntegerField(default=1 * 1024 * 1024 * 1024) #1GB
    used_storage_space = models.IntegerField(default=0)

    def storage_space_gb(self):
        return self.storage_space / 1073741824

    def used_storage_space_gb(self):
       return round(self.used_storage_space / 1073741824, 2)


