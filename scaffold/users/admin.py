from django.contrib import admin
from .models import Profile, Relationship, UserType

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(UserType)
