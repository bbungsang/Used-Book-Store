from django.conf import settings


def facebook_info(request):
    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'site_url': 'http://localhost:8000',
    }
    return context


def kakao_info(request):
    context = {
        'kakao_app_id': settings.KAKAO_APP_ID,
        'redirect_uri': settings.KAKAO_REDIRECT_URI,
    }
    return context