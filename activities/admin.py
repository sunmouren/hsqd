from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    活动后台管理
    """
    list_display = ['id', 'title', 'address', 'start_time', 'is_active']
