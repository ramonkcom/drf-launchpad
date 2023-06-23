from django.contrib.auth import get_user_model
from django.test import TestCase

from ..mixins import UserTestMixin
from ...models import Profile


User = get_user_model()


class UserModelTests(UserTestMixin,
                     TestCase):
    """Test cases for the `User` model.
    """

    def test_user_str(self):
        """`User` string representation is the username + email
        """

        user = self.create_user(email='test@test.com',
                                username='t3s7')
        self.assertEqual(str(user), 't3s7 (test@test.com)')

    def test_creating_user_creates_profile(self):
        """Creating an `User` also creates a `Profile`
        """

        self.assertEqual(Profile.objects.count(), 0)
        user = self.create_user()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first(), user.profile)

    def test_deleting_user_deletes_profile(self):
        """Deleting an `User` also deletes the `Profile`
        """

        self.assertEqual(Profile.objects.count(), 0)
        user = self.create_user()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first(), user.profile)

        user.delete()
        self.assertEqual(Profile.objects.count(), 0)

    def test_user_handles_profile_data(self):
        """`User` model handles profile data
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
        self.assertEqual(Profile.objects.count(), 0)

        user = None
        user = self.create_user(email='ramon@test.com',
                                password='test#password@123',
                                given_name='Ramon',
                                family_name='Kayo')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.first(), user.profile)

        self.assertEqual(user.given_name, 'Ramon')
        self.assertEqual(user.family_name, 'Kayo')

        self.assertEqual(user.profile.given_name, 'Ramon')
        self.assertEqual(user.profile.family_name, 'Kayo')

        # NOTE this test exists because `__getattr__` is being overriden in
        # the `User` model to handle `Profile` fields as it was its own
        with self.assertRaises(AttributeError):
            _test = user.inexistent_field
