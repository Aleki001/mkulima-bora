from django.contrib import admin

from .models import Image, SubscribedUsers

admin.site.register(Image)
admin.site.register(SubscribedUsers)