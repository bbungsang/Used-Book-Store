from django.conf import settings
from django.shortcuts import render


def profile(request):
    return render(request, 'member/profile.html')
