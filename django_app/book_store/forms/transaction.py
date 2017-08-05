from django import forms

from book_store.models import BookSellBucket, Transaction, Book


class SellBookForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'book',
            'sell_price',
        ]
