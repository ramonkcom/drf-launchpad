from django.core import exceptions
from django.test import TransactionTestCase

from ...models import Profile
from ..mixins import UserTestMixin


class ProfileModelTests(UserTestMixin,
                        TransactionTestCase):
    """Test cases for the `Profile` model.
    """

    def test_profile_str(self):
        """`Profile` string representation is the full name, or user
        """

        user = self.create_user(email='rk1@teste.com',
                                given_name='Ramon',
                                family_name='Kayo')
        self.assertEqual(str(user.profile), 'Ramon Kayo')

        user = self.create_user(email='rk2@teste.com',
                                given_name='Ramon',
                                family_name=None)
        self.assertEqual(str(user.profile), 'Ramon')

        user = self.create_user(email='rk3@teste.com',
                                given_name=None,
                                family_name=None)
        self.assertEqual(str(user.profile), f'{user.username} ({user.email})')

    def test_delete_profile_forbidden(self):
        """It's impossible to delete `Profile` instances directly
        """

        self.assertEqual(Profile.objects.count(), 0)
        user = self.create_user()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first(), user.profile)

        with self.assertRaises(exceptions.PermissionDenied):
            user.profile.delete()
        self.assertEqual(Profile.objects.count(), 1)

        with self.assertRaises(exceptions.PermissionDenied):
            Profile.objects.first().delete()
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_profile_without_user_forbidden(self):
        """It's impossible to create `Profile` instances directly
        """

        self.assertEqual(Profile.objects.count(), 0)

        with self.assertRaises(Exception):
            Profile.objects.create(given_name='John',
                                   family_name='Doe')

        self.assertEqual(Profile.objects.count(), 0)
