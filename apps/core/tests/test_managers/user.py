from datetime import datetime

from django.test import TestCase

from ...models import (
    Person,
    User,
)
from ..mixins import UserTestsMixin


class UserManagerTests(UserTestsMixin,
                       TestCase):
    """Test cases for the `UserManager` manager.
    """

    def test_manager_create_user_creates_username(self):
        """Usernames are generated when not provided
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        user_1 = self.create_user(email='test@example1.com')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user_1.username, 'test')

        user_2 = self.create_user(email='test@example2.com')
        auto_username = 'test_' + str(int(datetime.now().timestamp()))[-5:-2]
        self.assertTrue(user_2.username.startswith(auto_username))

    def test_manager_create_user_accepts_person_data(self):
        """`UserManager` handles personal data
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.create_user(
            email='valid.email@test.com',
            password='valid#password@123',
            given_name='Ramon',
            family_name='Kayo',
        )
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.first(), user.person)

        self.assertEqual(user.person.given_name, 'Ramon')
        self.assertEqual(user.person.family_name, 'Kayo')
