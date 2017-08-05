from django import forms


class SearchForm(forms.Form):
    q_search = forms.CharField(
        max_length=64,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search...',
            }
        )
    )

class PriceForm(forms.Form):
    price = forms.IntegerField(
        widget=forms.IntegerField(
            attrs={
                'placeholder': '희망가격',
            }
        )
    )