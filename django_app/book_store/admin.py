from django.contrib import admin

from django_extensions.admin import ForeignKeyAutocompleteAdmin

from .models import Book
from .models import Transaction
from .models import BookBuyBucket
from .models import BookSellBucket


class BookAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'title', 'price', 'writer', 'publisher', 'publication_date', 'isbn']


class TransactionAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'book', 'seller', 'buyer', 'is_successed', 'sell_price']


class BookBuyBucketAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'user', 'book']


class BookSellBucketAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ['id', 'user', 'book']

admin.site.register(Book, BookAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(BookBuyBucket, BookBuyBucketAdmin)
admin.site.register(BookSellBucket, BookSellBucketAdmin)
