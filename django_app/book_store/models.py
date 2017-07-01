from django.db import models

from config import settings


class BookInfo(models.Model):
    book_image = models.ImageField()
    writer = models.CharField(max_length=36)
    publisher = models.CharField(max_length=36)
    publication = models.CharField(max_length=12)

    original_price = models.CharField(max_length=12)
    used_price = models.CharField(max_length=12)
    sell_price1 = models.CharField(max_length=12)
    sell_price2 = models.CharField(max_length=12)
    sell_price3 = models.CharField(max_length=12)

    book_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='BookLike',
        related_name='like_books',
    )


class BookLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    book_info = models.ForeignKey(BookInfo, )
    created_at = models.DateTimeField(auto_now_add=True)


class SellBook(models.Model):
    book_info = models.ForeignKey(BookInfo, )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    sell_price = models.CharField(max_length=12)
    book_status = models.CharField(max_length=2)


class Comment(models.Model):
    book_info = models.ForeignKey(BookInfo, )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    pass
