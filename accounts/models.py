from myproj import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    storage_space = models.IntegerField(default=1 * 1024 * 1024 * 1024) #1GB

