from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from book_store.forms.transaction import SellBookForm
from book_store.models import Book, Transaction

User = get_user_model()


def check_buyers_and_send_email(isbn):
    """
    팔 책에 대한 구매자가 있는지 체크하여
    이메일을 전송한다.
    :param isbn:
    :return:
    """
    book_info = Book.objects.get(isbn=isbn)
    transactions = Transaction.objects.filter(buyer__isnull=False)

    for transaction in transactions:
        if transaction and transaction.book == book_info:
            mail_subject = '{}님께서 등록하신 `{}`에 대하여 판매 책 정보가 업데이트 되었습니다.'.format(
                transaction.buyer.username,
                book_info.title
            )
            mail_content = '책책책! 책을 읽읍시다!'
            # ToDo-https://docs.djangoproject.com/en/1.11/topics/email/#send-mass-mail
            send_mail(
                mail_subject,
                mail_content,
                settings.EMAIL_HOST_USER,
                [transaction.buyer.email],
            )


def register_sell_book(request, ):
    seller = get_object_or_404(User, pk=request.user.pk)

    if request.method == 'POST':
        form = SellBookForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.seller = seller
            post.save()

            isbn = post.book.isbn
            check_buyers_and_send_email(isbn)
        return HttpResponse('Hello World!')

    else:
        form = SellBookForm()
    context = {
        'form': form,
    }
    return render(request, 'books/register_test.html', context)