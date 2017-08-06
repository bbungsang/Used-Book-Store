from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMessage

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

    if request.method == 'POST':
        form = TransactionCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            mail_subject = '{}에 작성한 글에 {}님이 댓글을 작성했습니다'.format(
                post.created.strftime('%Y.%m.%d %H:%M'),
                request.user
            )
            mail_content = '< {}님의 댓글 >\n{}'.format(
                request.user,
                comment.content
            )
            send_mail(
                mail_subject,
                mail_content,
                settings.EMAIL_HOST_USER,
                [post.seller.email],
            )
        else:
            result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
            messages.error(request, result)
            # next 값이 존재하면 해당 주소로, 없으면 transaction_post_detail 로 이동
        # if next:
        #     return redirect(next)

        return HttpResponse('<h1>Hello World!</h1>')
    else:
        form = TransactionCommentForm()
    context = {
        'form': form,
    }

    return render(request, 'books/comment_test.html', context)