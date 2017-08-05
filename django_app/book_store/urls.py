from django.conf.urls import url

from . import views

app_name = 'books'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^book_search/$', views.book_search, name='book_search'),
    url(r'^book_bucket/$', views.book_bucket, name='book_bucket'),
    url(r'^detail/([0-9]+)/$', views.book_detail, name='book_detail'),

    # url(r'^book/comment/$', views.book_comment_create, name='book_comment_create'),
    url(r'^(?P<post_pk>\d+)/transaction/comment/$', views.transaction_comment_create, name='transaction_comment_create'),
]
