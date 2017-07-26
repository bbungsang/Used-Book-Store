from django.conf import settings
from django.db import models


class BookInfo(models.Model):
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
