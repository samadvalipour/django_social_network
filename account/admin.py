from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UA
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model= Profile
    can_delete= False

class UserAdmin(UA):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
