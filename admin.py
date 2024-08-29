from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInLine(admin.StackedInline):
    model = Profile


class ExentedUser(UserAdmin):
    inlines = [ProfileInLine]

admin.site.unregister(User)
admin.site.register(User, ExentedUser)