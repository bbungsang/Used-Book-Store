from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_model(self):
        """
        유저 생성 코드
        create_user 호출한 코드 수와 Row 개수가 적합한지,
        올바른 값이 삽입되는지 확인
        """

        user1 = User.objects.create_user(
            username='bbungsang',
            password='1234'
        )
        user1.save()

        user2 = User.objects.create_user(
            username='bazzi',
            password='1234'
        )
        user2.save()

        saved_users = User.objects.all()

        self.assertEqual(saved_users.count(), 2)

        first_saved_user = saved_users[0].username
        second_saved_user = saved_users[1].username
        self.assertEqual(first_saved_user, 'bbungsang')
        self.assertEqual(second_saved_user, 'bazzi')