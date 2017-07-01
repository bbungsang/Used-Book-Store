from django.contrib import admin

from book_store.models import BookInfo


class PostAdmin(admin.ModelAdmin):
    # list_display = ['id', 'writer', 'publisher', 'publication', 'original_price', 'used_price']
    pass
admin.site.register(BookInfo, PostAdmin)
