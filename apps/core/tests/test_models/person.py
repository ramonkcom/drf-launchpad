from django.core import exceptions
from django.test import TransactionTestCase

from ...models import Person
from ..mixins import UserTestMixin


class PersonModelTests(UserTestMixin,
                       TransactionTestCase):
    """Test cases for the `Person` model.
    """

    def test_person_str(self):
        """`Person` string representation is the full name, or user
        """

        user = self.create_user(email='rk1@teste.com',
                                given_name='Ramon',
                                family_name='Kayo')
        self.assertEqual(str(user.person), 'Ramon Kayo')

        user = self.create_user(email='rk2@teste.com',
                                given_name='Ramon',
                                family_name=None)
        self.assertEqual(str(user.person), 'Ramon')

        user = self.create_user(email='rk3@teste.com',
                                given_name=None,
                                family_name=None)
        self.assertEqual(str(user.person), f'{user.username} ({user.email})')

    def test_delete_person_forbidden(self):
        """It's impossible to delete `Person` instances
        """

        self.assertEqual(Person.objects.count(), 0)
        user = self.create_user()
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.first(), user.person)

        with self.assertRaises(exceptions.PermissionDenied):
            user.person.delete()
        self.assertEqual(Person.objects.count(), 1)

        with self.assertRaises(exceptions.PermissionDenied):
            Person.objects.first().delete()
        self.assertEqual(Person.objects.count(), 1)

    def test_create_person_without_user_forbidden(self):
        """It's impossible to create `Person` instances without an `User`
        """

        self.assertEqual(Person.objects.count(), 0)

        with self.assertRaises(Exception):
            Person.objects.create(given_name='John',
                                  family_name='Doe')

        self.assertEqual(Person.objects.count(), 0)
