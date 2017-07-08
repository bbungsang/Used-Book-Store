from django.contrib.auth import login as django_login, logout as django_logout
from django.shortcuts import render, redirect

from ..forms import SignupForm, LoginForm

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
            user = form.create_user()
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


def telegram():
    import requests
    from bs4 import BeautifulSoup
    import os
    import time

    import telegram
    from ..secret import telegram_token

    # 토큰을 지정해서 bot을 선언
    bot = telegram.Bot(token=telegram_token)

    # 만약 IndexError 에러가 난다면 봇에게 메시지를 아무거나 보내고 다시 테스트
    chat_id = bot.getUpdates()[-1].message.chat.id

    # 파일의 위치
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    while True:
        req = requests.get('http://www.onoffmix.com/event?c=85', headers={
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
        })
        req.encoding = 'utf-8'

        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.select('ul.todayEvent')
        latest = posts[1].text

        with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
            before = f_read.readline()
            if before != latest:
                bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!')
            else:  # 원래는 이 메시지를 보낼 필요가 없지만, 테스트 할 때는 봇이 동작하는지 확인차 넣어봤어요.
                bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')
            f_read.close()

        with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
            f_write.write(latest)
            f_write.close()

        time.sleep(60)
