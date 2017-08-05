from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Book(TimeStampedModel):
    """책 정보"""
    image_url = models.CharField("이미지url", max_length=240)
    title = models.CharField("제목", max_length=48)
    intro = models.TextField("소개", blank=True)
    writer = models.CharField("저자", max_length=36)
    price = models.IntegerField("정가")
    isbn = models.CharField("isbn", max_length=100, unique=True)
    publisher = models.CharField("출판사", max_length=40)
    publication_date = models.DateField("출판일")

    def __str__(self):
        return "{} {}".format(self.title, self.writer)


class Transaction(TimeStampedModel):
    """거래기록"""
    book = models.ForeignKey(Book)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="seller_set", verbose_name="판매자", null=True, default=None, blank=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="buyer_set", verbose_name="구매자", null=True, default=None, blank=True)
    is_successed = models.BooleanField("거래성사", default=False)
    sell_price = models.IntegerField("판매가")


class BookLike(TimeStampedModel):
    """책에 대한 좋아요"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book_info = models.ForeignKey(Book)


class Category(models.Model):
    pass


class BookBuyBucket(TimeStampedModel):
    """장바구니"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    transaction = models.ForeignKey(
        Transaction,
    )

    class Meta:
        unique_together = (("user", "transaction"),)


class BookSellBucket(TimeStampedModel):
    """판매자 판매 목록"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(
        Book,
    )
