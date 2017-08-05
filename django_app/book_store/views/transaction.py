from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from book_store.forms.transaction import SellBookForm
from book_store.models import Book, Transaction

User = get_user_model()


def check_buy_book(isbn):
    book_info = Book.objects.get(isbn=isbn)
    buyers = Transaction.objects.filter(buyer__isnull=False)

    for buyer in buyers:

        if buyer and buyer.book == book_info:
            mail_subject = '{}님께서 등록하신 `{}`에 대하여 판매 책 정보가 업데이트 되었습니다.'.format(
                buyer.buyer.username,
                book_info.title
            )
            mail_content = '책책책! 책을 읽읍시다!'
            send_mail(
                mail_subject,
                mail_content,
                settings.EMAIL_HOST_USER,
                [buyer.buyer.email],
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
            check_buy_book(isbn)
        return HttpResponse('Hello World!')

    else:
        form = SellBookForm()
    context = {
        'form': form,
    }
    return render(request, 'books/register_test.html', context)