from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from ..forms.transaction import SellBookForm
from ..models import Transaction
from ..models import Book
from ..models import BookBuyBucket
from ..forms import SearchForm

from ..api import get_book_info, register_book

User = get_user_model()


def main(request):
    books = Book.objects.all()
    context = {
        'books': books,
        'search': SearchForm(),
    }
    return render(request, 'books/main.html', context)


def book_detail(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    context = {
        'book': book,
    }
    return render(request, 'books/book_detail.html', context)


def book_search(request):

    # data 를 POST 요청으로 처리해서 form 변수에 할당
    form = SearchForm(data=request.POST)

    # is_valid() 를 통해 data clean 과정을 거쳐 폼 유효성을 검사한다.
    if form.is_valid():

        # 사용자가 입력한 순수 검색어를 q 에 할당
        q = form.cleaned_data['q_search']

        # BookInfo 테이블의 title, writer, publisher 필드에 q 가 속한 레코드를 book_lists 에 할당
        book_lists = Book.objects.filter(
            Q(Q(title__contains=q) | Q(writer__contains=q)) | Q(publisher__contains=q),
        )

        # 템플릿에 보이기 위한 필요한 데이터를 인자로 전달
        context = {
            'q': q,
            'book_lists': book_lists,
            'book_count': book_lists.count(),
            'search': SearchForm(),
        }

        return render(request, 'books/book_list.html', context)


def book_bucket(request):
    if request.method == 'POST':

        # input 태그 name="book_id" 에 해당하는 value 를 book_id 에 할당
        book_id = request.POST['book_id']

        # book_id 에 해당하는 BookInfo 테이블의 레코드를 book_info 에 할당
        book_info = get_object_or_404(Book, pk=book_id)

        # BookBuyBucket 을 역참조하여 로그인 한 유저가 선택한 책 정보가 담긴 레코드 생성
        # 장바구니는 책을 중복할 수 있으므로 get_or_create 가 아닌 create 활용
        book_info.bookbuybucket_set.create(
            user=request.user,
            book=book_info,
        )

        # book_lists = book_info.BookBuyBucket_set.filter(user_id=request.user.id)
        # 질문) 아래 코드와 뭐가 다른건지 모르겠다.

        # BookBuyBucket 테이블에서 user id 에 해당하는 레코드를 전부 book_lists 에 할당(객체의 iterable 형태)
        book_lists = BookBuyBucket.objects.filter(user_id=request.user.id)

        # 템플릿에 전달할 인자인 books 선언
        books = []

        # iterable 형태인 book_lists 를 for 문으로 분리시키고,
        for book_list in book_lists:

            # 분리된 BookBuyBucket 레코드의 book_id 에 해당하는 BookInfo 의 정보를 순차적으로 books 에 append
            books.append(Book.objects.get(pk=book_list.book_id))

        context = {
            'books': books,
        }
        return render(request, 'books/book_bucket.html', context)
    else:
        book_lists = BookBuyBucket.objects.filter(user_id=request.user.id)

        books = []

        for book_list in book_lists:
            books.append(Book.objects.get(pk=book_list.book_id))

        context = {
            'books': books,
        }
        return render(request, 'books/book_bucket.html', context)


def book_sell_list(request):
    sell_transactions = Transaction.objects.filter(
        is_successed=False, buyer__isnull=True, seller__isnull=False
    ).prefetch_related('book')
    return render(request, 'books/sell_list.html', {'sell_transactions': sell_transactions})


def book_buy_list(request):
    pass


def book_bucket_save(request, transaction_pk):
    '''
    책 찜하기
    :param request: Request
    :param transaction_pk: Transaction
    '''
    transaction = get_object_or_404(
        Transaction, pk=transaction_pk)
    try:
        BookBuyBucket.objects.create(
            user=request.user, transaction=transaction)
    except IntegrityError:
        return redirect('books:book_sell_list')
    return redirect('books:book_bucket_list')


def book_bucket_list(request):
    '''
    찜한 책 리스트
    :param request: Request
    '''
    items = BookBuyBucket.objects.filter(
        user=request.user
    ).prefetch_related(
        'transaction', 'transaction__book'
    )
    return render(request, 'books/book_bucket.html', {'items': items})


def book_sell_register(request):
    keyword = request.GET.get('keyword')
    items = None
    if keyword:
        items = get_book_info(keyword)
    datas = []
    if items:
        for item in items:
            book = register_book(isbn=item['isbn'])[1]
            form = SellBookForm(initial={'book': book})
            datas.append([item, form])
    return render(request, 'books/book_sell_register.html', {'datas': datas})

def book_sell_register_save(request):
    if request.method == 'POST':
        form = SellBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
        return redirect('books:book_sell_list')