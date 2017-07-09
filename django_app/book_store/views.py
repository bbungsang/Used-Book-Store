from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SearchForm
from .models import BookInfo, BookBucket

User = get_user_model()

def main(request):
    books = BookInfo.objects.all()
    context = {
        'books': books,
        'search': SearchForm(),
    }
    return render(request, 'books/main.html', context)


def book_detail(request, book_pk):
    book = BookInfo.objects.get(pk=book_pk)
    context = {
        'book': book,
    }
    return render(request, 'books/book_detail.html', context)


def book_search(request):
    form = SearchForm(data=request.POST)
    if form.is_valid():
        q = form.cleaned_data['q_search']
        book_lists = BookInfo.objects.filter(
            Q(Q(title__contains=q) | Q(writer__contains=q)) | Q(publisher__contains=q),
        )

        context = {
            'q': q,
            'book_lists': book_lists,
            'book_count': book_lists.count(),
            'search': SearchForm(),
        }
        return render(request, 'books/book_list.html', context)


def book_bucket(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        book_info = get_object_or_404(BookInfo, pk=book_id)
        book_info.bookbucket_set.create(
            user=request.user,
            book=book_info,
        )

        # book_lists = book_info.bookbucket_set.filter(user_id=request.user.id)
        book_lists = BookBucket.objects.filter(user_id=request.user.id)

        books = []

        for book_list in book_lists:
            books.append(BookInfo.objects.get(pk=book_list.book_id))

        context = {
            'books': books,
        }
        return render(request, 'books/book_bucket.html', context)
    else:
        return redirect('books/book_list')
