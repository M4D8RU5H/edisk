from django.db import models
from myproj import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    storage_space = models.FloatField(default=0.0)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='user_set_mainapp')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='user_set_mainapp')


class file_upload(models.Model):
    ids = models.AutoField(primary_key=True)
    my_file = models.FileField(upload_to='')
    
    
    def __str__(self):
        return self.my_file
    
class FileModel(models.Model):
    ids = models.AutoField(primary_key=True)
    file = models.FileField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.FilePathField(path=settings.MEDIA_ROOT, default=settings.MEDIA_ROOT)
