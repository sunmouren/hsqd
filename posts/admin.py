from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    文章管理
    """
    list_display = ['id', 'title', 'user', 'created', 'is_active']
