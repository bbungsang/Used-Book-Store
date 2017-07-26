from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager


class UserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id'],
        )

        user, user_created = self.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'email': user_info.get('email', ''),
            }
        )
        return user


class User(AbstractUser):
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )

    objects = UserManager()

    # profile_img = models.ImageField(blank=True)
    email = models.EmailField(null=True, unique=True)

    # 유저타입. 기본은 Django, 페이스북 로그인 시 USER_TYPE_FACEBOOK 값을 갖음
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)