from django import forms

from ..models import BookSellBucket, Transaction, Book


class SellBookForm(forms.ModelForm):
    # book = forms.ModelChoiceField(initial={'username': costumer.username})

    class Meta:
        model = Transaction
        fields = [
            'book',
            'sell_price',
        ]
        widgets = {'book': forms.HiddenInput()}
