from django.conf.urls import url

from . import views

app_name = 'books'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^book/sell/list$', views.book_sell_list, name='book_sell_list'),
    url(r'^book/sell/register$', views.book_sell_register, name='book_sell_register'),
    url(r'^book/bucket/(?P<transaction_pk>\d+)/save$', views.book_bucket_save, name='book_bucket_save'),
    url(r'^book/bucket/list$', views.book_bucket_list, name='book_bucket_list'),
    url(r'^book/buy/list$', views.book_buy_list, name='book_buy_list'),
    url(r'^book_search/$', views.book_search, name='book_search'),
    url(r'^book_bucket/$', views.book_bucket, name='book_bucket'),
    url(r'^detail/(?P<book_pk>\d+)/$', views.book_detail, name='book_detail'),

    # url(r'^book/comment/$', views.book_comment_create, name='book_comment_create'),
    url(r'^(?P<post_pk>\d+)/transaction/comment/$', views.transaction_comment_create, name='transaction_comment_create'),
]
