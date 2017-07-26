from django.conf.urls import url

from . import views

app_name = 'books'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^book_search/$', views.book_search, name='book_search'),
    url(r'^book_bucket/$', views.book_bucket, name='book_bucket'),
]
