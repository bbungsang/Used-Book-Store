from django.contrib import admin

from .models import BookInfo


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'writer', 'publisher', 'publication']
admin.site.register(BookInfo, PostAdmin)
