import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.shortcuts import render, redirect

from ..utils.exceptions.social_login import DebugTokenException, GetAccessTokenException
from ..forms import SignupForm, LoginForm

User = get_user_model()

__all__ = (
    'signup',
    'login',
    'logout',
)


def login(request):
    # telegram()

    form = LoginForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            return redirect('books:main')
    else:
        if request.user.is_authenticated():
            return redirect('books:main')
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('member:login')


def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('member:my_profile')
        else:
            context = {
                'form': form,
            }
            return render(request, 'member/signup.html', context)
    form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)

##
# 소셜 로그인(페이스북, 카카오)
##


def facebook_login(request):

    # 페이스북 로그인 버튼의 URL 을 통하여 facebook_login view 가 처음 호출될 때, 'code' request GET parameter 받으며, 'code' 가 없으면 오류 발생한다.
    code = request.GET.get('code')

    ##
    # 액세스 토큰 얻기
    ##

    # code 인자를 받아서 Access Token 교환을 URL 에 요청후, 해당 Access Token 을 받는다.
    def get_access_token(code):

        # Access Token 을 교환할 URL
        exchange_access_token_url = 'https://graph.facebook.com/v2.9/oauth/access_token'

        # 이전에 요청했던 URL 과 같은 값 생성(Access Token 요청시 필요)
        redirect_uri = '{}{}'.format(
            settings.SITE_URL,
            request.path,
        )

        # # Access Token 을 교환할 URL
        # exchange_access_token_url = 'https://graph.facebook.com/v2.9/oauth/access_token'

        # Access Token 요청시 필요한 파라미터
        exchange_access_token_url_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        print(exchange_access_token_url_params)

        # Access Token 을 요청한다.
        response = requests.get(
            exchange_access_token_url,
            params=exchange_access_token_url_params,
        )
        result = response.json()
        print(result)

        # 응답받은 결과값에 'access_token'이라는 key 가 존재하면,
        if 'access_token' in result:
            # access_token key 의 value 를 반환한다.
            return result['access_token']
        elif 'error' in result:
            raise Exception(result)
        else:
            raise Exception('Unknown error')

    ##
    # 액세스 토큰이 올바른지 검사
    ##
    def debug_token(token):
        app_access_token = '{}|{}'.format(
            settings.FACEBOOK_APP_ID,
            settings.FACEBOOK_SECRET_CODE,
        )

        debug_token_url = 'https://graph.facebook.com/debug_token'
        debug_token_url_params = {
            'input_token': token,
            'access_token': app_access_token
        }

        response = requests.get(debug_token_url, debug_token_url_params)
        result = response.json()

        if 'error' in result['data']:
            raise DebugTokenException(result)
        else:
            return result


    ##
    # 에러 메세지를 request 에 추가, 이전 페이지로 redirect
    ##
    def add_message_and_redirect_referer():
        error_message = 'Facebook login error'
        messages.error(request, error_message)

        # 이전 URL 로 리다이렉트
        return redirect(request.META['HTTP_REFERER'])

    ##
    # 발급받은 Access Token 을 이용하여 User 정보에 접근
    ##
    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/{user_id}'.format(user_id=user_id)
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'email',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result

    ##
    # 페이스북 로그인을 위해 정의한 함수 실행하기
    ##

    # code 가 없으면 에러 메세지를 request 에 추가하고 이전 페이지로 redirect
    if not code:
        return add_message_and_redirect_referer()

    try:
        access_token = get_access_token(code)
        debug_result = debug_token(access_token)
        user_info = get_user_info(user_id=debug_result['data']['user_id'], token=access_token)
        user = User.objects.get_or_create_facebook_user(user_info)

        django_login(request, user)
        return redirect('books:main')
    except GetAccessTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()


def kakao_login(request):
    code = request.GET.get('code')

    ##
    # 액세스 토큰 얻기
    ##

    # code 인자를 받아서 Access Token 교환을 URL 에 요청후, 해당 Access Token 을 받는다.
    def get_access_token(code):

        # Access Token 을 교환할 URL
        exchange_access_token_url = 'https://kauth.kakao.com/oauth/token'

        # 이전에 요청했던 URL 과 같은 값 생성(Access Token 요청시 필요)
        redirect_uri = settings.KAKAO_REDIRECT_URI

        # Access Token 요청시 필요한 파라미터
        exchange_access_token_url_params = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_APP_ID,
            'redirect_uri': redirect_uri,
            'code': code,
            'client_secret': settings.KAKAO_CLIENT_SECRET,
        }

        # Access Token 을 요청한다.
        response = requests.get(
            exchange_access_token_url,
            params=exchange_access_token_url_params,
        )
        result = response.json()
        print("get_access_token result :", result)

        # 응답받은 결과값에 'access_token'이라는 key 가 존재하면,
        if 'access_token' in result:
            # access_token key 의 value 를 반환한다.
            return result['access_token']
        elif 'error' in result:
            raise Exception(result)
        else:
            raise Exception('Unknown error')

    def add_message_and_redirect_referer():
        error_message = 'Kakao login error'
        messages.error(request, error_message)

        # 이전 URL 로 리다이렉트
        return redirect(request.META['HTTP_REFERER'])

    def app_connection(access_token):
        url = 'https://kapi.kakao.com/v1/user/signup'
        access_token = "Bearer " + access_token
        response = requests.get(
            url,
            headers={
                "Authorization": access_token,
                "Content-Type": "Content-Type: application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        print(response)
        result = response.json()
        print('app_connection result :', result)
        return result

    ##
    # 발급받은 Access Token 을 이용하여 User 정보에 접근
    ##
    def get_user_info(app_connection):
        url = 'https://kapi.kakao.com/v1/user/me'
        # url_user_info_params = {
        #     'target_id_type': 'user_id',
        #     'target_id': app_connection,
        #     'propertyKeys': [
        #         'name',
        #     ]
        # }
        response = requests.get(
            url,
            headers={
                "Authorization": "Bearer " + access_token,
                # "Content-Type": "Content-Type: application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        result = response.json()
        # 요청이 성공하면 응답 바디에 JSON 객체로 id, kaccount_email 을 포함한다.
        return result

    ##
    # 카카오 로그인을 위해 정의한 함수 실행하기
    ##

    # code 가 없으면 에러 메세지를 request 에 추가하고 이전 페이지로 redirect
    if not code:
        return add_message_and_redirect_referer()

    try:
        access_token = get_access_token(code)
        # debug_result = debug_token(access_token)
        app_connection = app_connection(access_token)
        user_info = get_user_info(app_connection)
        user = User.objects.get_or_create_kakao_user(user_info)

        django_login(request, user)
        return redirect('books:main')
    except GetAccessTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()


# def telegram(request):
#     import requests
#     from bs4 import BeautifulSoup
#     import os
#     import time
#
#     import telegram
#     from ..secret import telegram_token
#
#     # 토큰을 지정해서 bot을 선언
#     bot = telegram.Bot(token=telegram_token)
#
#     # 만약 IndexError 에러가 난다면 봇에게 메시지를 아무거나 보내고 다시 테스트
#     chat_id = bot.getUpdates()[-1].message.chat.id
#
#     # 파일의 위치
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
#     while True:
#         req = requests.get('http://www.onoffmix.com/event?c=85', headers={
#             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
#         })
#         req.encoding = 'utf-8'
#
#         html = req.text
#         soup = BeautifulSoup(html, 'html.parser')
#         posts = soup.select('ul.todayEvent')
#         latest = posts[1].text
#
#         with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
#             before = f_read.readline()
#             if before != latest:
#                 bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!')
#             else:  # 원래는 이 메시지를 보낼 필요가 없지만, 테스트 할 때는 봇이 동작하는지 확인차 넣어봤어요.
#                 bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')
#             f_read.close()
#
#         with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
#             f_write.write(latest)
#             f_write.close()
#
#         time.sleep(60)
