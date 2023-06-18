from django.contrib.auth import get_user_model
from django.test import TestCase

from ..mixins import UserTestsMixin
from ...models import Person


User = get_user_model()


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

    def test_user_handles_personal_data(self):
        """`User` model handles personal data
        """

        user = User(given_name='Ramon',
                    family_name='Kayo')

        self.assertEqual(user.given_name, 'Ramon')
        self.assertEqual(user.family_name, 'Kayo')

        user.given_name = 'Ramon Test'
        user.family_name = 'Kayo Test'

        self.assertEqual(user.given_name, 'Ramon Test')
        self.assertEqual(user.family_name, 'Kayo Test')

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 0)

        user = None
        user = self.create_user(email='ramon@test.com',
                                password='test#password@123',
                                given_name='Ramon',
                                family_name='Kayo')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.first(), user.person)

        self.assertEqual(user.given_name, 'Ramon')
        self.assertEqual(user.family_name, 'Kayo')

        self.assertEqual(user.person.given_name, 'Ramon')
        self.assertEqual(user.person.family_name, 'Kayo')

        # NOTE this test exists because `__getattr__` is being overriden in
        # the `User` model to handle `Person` fields as it was its own
        with self.assertRaises(AttributeError):
            _test = user.inexistent_field
