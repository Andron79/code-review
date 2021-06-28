from django.contrib import admin
from app.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['inn', 'balance']


admin.site.register(UserProfile, UserProfileAdmin)
