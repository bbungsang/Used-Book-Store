from django.contrib import admin

from book_store.models import BookInfo


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'writer', 'publisher', 'publication']
admin.site.register(BookInfo, PostAdmin)
