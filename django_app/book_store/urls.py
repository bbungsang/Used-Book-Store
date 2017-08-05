from django.conf.urls import url

from . import views

app_name = 'books'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^book_search/$', views.book_search, name='book_search'),
    url(r'^book_bucket/$', views.book_bucket, name='book_bucket'),
    url(r'^detail/(?P<book_id>\d+)/$', views.book_detail, name='book_detail'),
    url(r'^detail/(?P<book_id>\d+)/buy/$', views.book_buy, name='book_buy'),
    url(r'^detail/(?P<book_id>\d+)/sell/$', views.book_sell, name='book_sell'),
]
