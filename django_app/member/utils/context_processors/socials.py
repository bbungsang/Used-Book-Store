from django.conf import settings


def facebook_info(request):
    context = {
        'facebook_app_id': settings.FACEBOOK_APP_ID,
        'site_url': 'http://localhost:8000',
    }
    return context