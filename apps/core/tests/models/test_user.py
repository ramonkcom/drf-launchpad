from datetime import datetime

from django.test import TestCase

from ...models import (
    Person,
    User,
)
from ..mixins import UserTestsMixin


class UserModelTests(UserTestsMixin,
                     TestCase):
    """Test cases for the `User` model.
    """

    def test_user_str(self):
        """`User` string representation is the username + email
        """

        user = self.create_user(email='test@test.com',
                                username='t3s7')
        self.assertEqual(str(user), 't3s7 (test@test.com)')

    def test_manager_create_user_creates_username(self):
        """`UserManager.create_user` creates username when not provided
        """

        self.assertEqual(User.objects.count(), 0)
        user_1 = self.create_user(email='test@example1.com')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user_1.username, 'test')

        user_2 = self.create_user(email='test@example2.com')
        auto_username = 'test_' + str(int(datetime.now().timestamp()))[-5:-2]
        self.assertTrue(user_2.username.startswith(auto_username))

    def test_creating_user_creates_person(self):
        """Creating an `User` also creates a `Person`
        """

        self.assertEqual(Person.objects.count(), 0)
        user = self.create_user()
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.first(), user.person)

    def test_deleting_user_deletes_person(self):
        """Deleting an `User` also deletes the `Person`
        """

        self.assertEqual(Person.objects.count(), 0)
        user = self.create_user()
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.first(), user.person)

        user.delete()
        self.assertEqual(Person.objects.count(), 0)

    def test_manager_create_user_accepts_person_data(self):
        """`UserManager.create_user` accepts personal data
        """

        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(
            email='valid.email@test.com',
            password='valid#password@123',
            person={
                'given_name': 'Ramon',
                'family_name': 'Kayo',
            }
        )
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.first(), user.person)

        self.assertEqual(user.person.given_name, 'Ramon')
        self.assertEqual(user.person.family_name, 'Kayo')
