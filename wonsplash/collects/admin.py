from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = ["id", "file", "creator", "views"]
    list_filter = ["id", "file"]
    list_display_links = ["id", "file"]


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):

    list_display = ["id", "image", "creator"]
    list_filter = ["id"]
    list_display_links = ["id"]
