from django import forms


from ..models import BookComment, TransactionComment


class BookCommentForm(forms.ModelForm):
    model = BookComment
    fields = [
        'content',
    ]
    widgets = {
        'content': forms.TextInput(
            attrs={
                'class': 'input-comment',
                'placeholder': '댓글 입력',
            }
        )
    }


class TransactionCommentForm(forms.ModelForm):
    model = TransactionComment
    fields = [
        'content',
    ]
    widgets = {
        'content': forms.TextInput(
            attrs={
                'class': 'input-comment',
                'placeholder': '댓글 입력',
            }
        )
    }