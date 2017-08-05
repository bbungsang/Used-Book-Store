from django.contrib import admin

from django_extensions.admin import ForeignKeyAutocompleteAdmin

from .models import Book, TransactionComment
from .models import Transaction
from .models import BookBuyBucket
from .models import BookSellBucket


class BookAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'title', 'price', 'writer', 'publisher', 'publication_date', 'isbn']
    search_fields = ['title', 'writer', 'isbn']


class TransactionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'book', 'seller', 'buyer', 'is_successed', 'sell_price']
    raw_id_fields = ['book', 'seller', 'buyer']
    search_fields = ['id', 'book__title', 'seller__username', 'buyer__username']


class BookBuyBucketAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'user', 'book']
    raw_id_fields = ['user', 'book']
    search_fields = ['id', 'user__username', 'user__email']


class BookSellBucketAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'user', 'book']
    raw_id_fields = ['user', 'book']
    search_fields = ['id', 'user__username', 'user__email']


class TransactionCommentCreateAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'post', 'author', 'content']
    raw_id_fields = ['post', 'author']
    # search_fields = ['']

admin.site.register(Book, BookAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(BookBuyBucket, BookBuyBucketAdmin)
admin.site.register(BookSellBucket, BookSellBucketAdmin)
admin.site.register(TransactionComment, TransactionCommentCreateAdmin)