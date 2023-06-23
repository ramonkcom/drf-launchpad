from datetime import datetime

from django.test import TestCase

from ...models import (
    Profile,
    User,
)
from ..mixins import UserTestMixin


class UserManagerTests(UserTestMixin,
                       TestCase):
    """Test cases for the `UserManager` manager.
    """

    def test_manager_create_user_creates_username(self):
        """`UserManager.create_user` generates username when not provided
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        user_1 = User.objects.create_user(email='test@example1.com')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user_1.username, 'test')

        user_2 = User.objects.create_user(email='test@example2.com')
        auto_username = 'test_' + str(int(datetime.now().timestamp()))[-5:-2]
        self.assertTrue(user_2.username.startswith(auto_username))

    def test_manager_create_user_accepts_profile_data(self):
        """`UserManager.create_user` handles profile data
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)
        user = self.create_user(
            email='valid.email@test.com',
            password='valid#password@123',
            given_name='Ramon',
            family_name='Kayo',
        )
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first(), user.profile)

        self.assertEqual(user.given_name, 'Ramon')
        self.assertEqual(user.family_name, 'Kayo')
        self.assertEqual(user.profile.given_name, 'Ramon')
        self.assertEqual(user.profile.family_name, 'Kayo')
