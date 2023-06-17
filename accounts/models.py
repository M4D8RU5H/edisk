from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    storage_space = models.FloatField(default=0.0)
