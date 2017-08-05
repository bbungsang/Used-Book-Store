from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'input-id',
            }
        )
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
            'placeholder': 'Password',
            'class': 'input-password',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=password,
        )
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                '. 다시 로그인하시거나, 회원가입해주세요.'
            )
        return self.cleaned_data
