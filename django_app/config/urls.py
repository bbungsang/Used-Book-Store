"""used-book-store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from config import settings
from rest_framework.authtoken import views
from django_messages.views import *
from member.forms import NewComposeForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^book/', include('book_store.urls', namespace="book_store")),
    url(r'^member/', include('member.urls', namespace="member")),
    url(r'^messages/compose/$', compose, {'form_class': NewComposeForm,}, name='messages_compose'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
urlpatterns += static('/static/', document_root='project/.static_root')
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
