from django.contrib import admin
from .models import User
from .models import file_upload
from .forms import CustomUserChangeForm

admin.site.register(file_upload)
admin.site.register(User)
#admin.site.register(User, form=CustomUserChangeForm)

