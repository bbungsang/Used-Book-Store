import re

from django import forms
from ..models import User


class SignupForm(forms.Form):
    img_profile = forms.ImageField()
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디를 입력하세요',
            }
        )
    )
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '원하시는 닉네임을 입력하세요',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 한번 더 입력하세요',
            }
        )
    )
    slack = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'example@example.com (필수입력)',
            }
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '000-0000-0000 (필수입력)',
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("해당 아이디는 사용할 수 없습니다. 다른 아이디를 입력하세요.")
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("해당 닉네임은 이미 사용중입니다. 다른 닉네임을 입력하세요.")
        return nickname

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 서로 일치하지 않습니다. 다시 입력해주세요.")
        return password2

    def clean_slack(self):
        slack = self.cleaned_data.get('slack')
        if slack and User.objects.filter(slack=slack).exists():
            raise forms.ValidationError('이미 등록된 슬랙 계정입니다.')
        return slack

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_strip = re.compile(r'^(?P<first>[0-9]{2,3})[-.](?P<second>[0-9]{3,4})[-.](?P<third>[0-9]{4}$)')

        phone_number = phone_strip.match(phone)
        if phone_number is None:
            raise forms.ValidationError('휴대전화번호가 올바르지 않습니다. 양식대로 입력하세요.')
        print('phone_number: ', phone_number)
        phone_val = phone_number.groups()
        print('phone_val: ', phone_val)
        print(phone_val[0])
        num_valid = phone_val[0] + phone_val[1] + phone_val[2]

        if num_valid and User.objects.filter(phone=phone_val).exists():
            raise forms.ValidationError('이미 등록된 전화번호입니다.')
        return num_valid

    def create_user(self):
        img_profile = self.cleaned_data['img_profile']
        username = self.cleaned_data['username']
        nickname = self.cleaned_data['nickname']
        password = self.cleaned_data['password1']
        slack = self.cleaned_data['slack']
        phone = self.cleaned_data['phone']
        new_user = User.objects.create_user(
            img_profile=img_profile,
            username=username,
            nickname=nickname,
            password=password,
            slack=slack,
            phone=phone,
        )
        return new_user

