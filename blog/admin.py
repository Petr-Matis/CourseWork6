from django.contrib import admin
from blog.models import *


# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Клиенты"""
    list_display = ('header', 'content', 'image', 'date_of_create', 'quantity_of_views')
    list_filter = ('date_of_create', 'quantity_of_views')
    search_fields = ('header', 'content', 'date_of_create',)
