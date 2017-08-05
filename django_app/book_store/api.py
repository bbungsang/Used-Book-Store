from datetime import date, datetime
from django.conf import settings
import json
import re
import urllib.request
import ssl

from .models import Book


def get_book_info(title=None, isbn=None, display='3', sort='count'):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET

    if title:
        enc_text = urllib.parse.quote(title)
        url = "https://openapi.naver.com/v1/search/book_adv?d_titl=" + enc_text +"&display="+ display + "&sort=" + sort
    if isbn:
        enc_text = urllib.parse.quote(isbn)
        url = "https://openapi.naver.com/v1/search/book_adv?d_isbn=" + enc_text
    search_request = urllib.request.Request(url)
    search_request.add_header("X-Naver-Client-Id", client_id)
    search_request.add_header("X-Naver-Client-Secret", client_secret)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(search_request, context=context)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        json_rt = response_body.decode('utf-8')
        py_rt = json.loads(json_rt)
        items = py_rt["items"]

        return items

    else:
        print("Error Code:" + rescode)


def register_book(isbn, model=Book):
    """
    해당 도서를 Book 모델 DB 혹은 WishBook 모델 저장한다. 이미 존재하는 경우 저장을 취소한다.
    isbn 정보를 활용하여 api 검색을 통해 책 정보를 가져온다.
    """
    if model.objects.filter(isbn=isbn).exists():
        message = '이미 존재하는 책입니다'
        return message, None

    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    isbn = urllib.parse.quote(isbn)
    url = "https://openapi.naver.com/v1/search/book_adv?d_isbn=" + isbn
    search_request = urllib.request.Request(url)
    search_request.add_header("X-Naver-Client-Id", client_id)
    search_request.add_header("X-Naver-Client-Secret", client_secret)
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(search_request, context=context)
    rescode = response.getcode()
    if rescode==200:
        response_body = response.read()
        json_rt = response_body.decode('utf-8')
        py_rt = json.loads(json_rt)
        item = py_rt["items"][0]

        TAG_RE = re.compile(r'<[^>]+>')

        book = model.objects.create(
            title=TAG_RE.sub('', item['title']),
            writer=TAG_RE.sub('', item['author']),
            publisher=TAG_RE.sub('', item['publisher']),
            intro=TAG_RE.sub('', item['description']),
            image_url=item['image'],
            isbn=item['isbn'],
            price=int(item['price']),
            publication_date=datetime.strptime(item['pubdate'], "%Y%m%d").date(),
        )
        message, book = '등록완료!', book
        return message, book

    else:
        message = "Error Code:" + rescode
        return message, None
