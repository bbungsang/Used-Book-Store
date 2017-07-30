from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from . import views_api


app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),

    # social login
    url(r'^login/facebook/$', views.facebook_login, name='facebook_login'),
    url(r'^login/kakao/$', views.kakao_login, name='kakao_login'),

    ##
    # api
    ##

    # FBV
    # url(r'^api/$', views_api.user_list),
    # url(r'^api/(?P<pk>[0-9]+)/$', views_api.user_detail),

    # CBV
    url(r'^api/$', views_api.UserList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views_api.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)