from django.test import TestCase

from ..mixins import UserTestsMixin
from ...models import Person


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
