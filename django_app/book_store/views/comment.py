from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from book_store.forms import TransactionCommentForm
from book_store.models import Transaction

__all__ = (
    'book_comment_create',
    'transaction_comment_create',
)


# @require_POST
# @login_required
def book_comment_create(request, book_pk):
    pass


# @require_POST
# @login_required
def transaction_comment_create(request, post_pk):
    post = get_object_or_404(Transaction, pk=post_pk)

    form = TransactionCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return HttpResponse('<h1>Hello World!</h1>')