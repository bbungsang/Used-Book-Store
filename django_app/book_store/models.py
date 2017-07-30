from django.conf import settings
from django.db import models

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class BookInfo(models.Model):
    objects = None
    image = models.ImageField()
    title = models.CharField(max_length=48)
    intro = models.TextField(blank=True)
    writer = models.CharField(max_length=36)
    publisher = models.CharField(max_length=36)
    publication = models.CharField(max_length=12)

    original_price = models.CharField(max_length=12)
    used_price = models.CharField(max_length=12, blank=True)
    sell_price1 = models.CharField(max_length=12, blank=True)
    sell_price2 = models.CharField(max_length=12, blank=True)
    sell_price3 = models.CharField(max_length=12, blank=True)

    book_bucket = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BookBucket',
        related_name='book_bucket'
    )

    book_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BookLike',
        related_name='like_books',
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='book_info')
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        `pygments` 라이브러리를 사용하여 하이라이트된 코드 생성
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(BookInfo, self).save(*args, **kwargs)


class BookLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book_info = models.ForeignKey(BookInfo, )
    created_at = models.DateTimeField(auto_now_add=True)


class SellBook(models.Model):
    book_info = models.ForeignKey(BookInfo, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sell_price = models.CharField(max_length=12)
    book_status = models.CharField(max_length=2)


class Comment(models.Model):
    book_info = models.ForeignKey(BookInfo, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    pass


class BookBucket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(
        BookInfo,
    )
    create_at = models.DateTimeField(auto_now=True)
