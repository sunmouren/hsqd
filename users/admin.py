from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    用户后台管理
    """
    list_display = ['id', 'username', 'email']
