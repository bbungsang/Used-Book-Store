from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'member'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),

    # social login
    url(r'^login/facebook/$', views.facebook_login, name='facebook_login'),
    url(r'^login/kakao/$', views.kakao_login, name='kakao_login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
