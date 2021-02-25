from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

admin.site.register(NewUser, UserAdmin)