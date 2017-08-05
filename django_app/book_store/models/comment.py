from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from book_store.models.book import Book, Transaction


class BookComment(TimeStampedModel):
    book_info = models.ForeignKey(Book, verbose_name='책 정보')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()


class TransactionComment(TimeStampedModel):
    post = models.ForeignKey(Transaction, verbose_name='거래 정보')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='댓글 작성자')
    content = models.TextField('댓글 내용')