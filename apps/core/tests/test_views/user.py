from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from utils.tests.mixins import APITestMixin

from ..mixins import UserTestMixin
from ...models import User


class UserCreateAPITests(UserTestMixin,
                         APITestMixin,
                         TestCase):

    def setUp(self):
        super().setUp()
        self.create_view = 'core:user-create'

    def test_create_user_valid_data(self):
        """It's possible to create a user with valid data
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        data = self.create_user_payload()
        res = self.api_create(data=data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertTrue(user_created)

    def test_create_user_invalid_password(self):
        """It's impossible to create an user with invalid password
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        data = self.create_user_payload(
            password_1='valid_pass!123',
            password_2='different#pass!456',
        )
        res = self.api_create(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_2', res.data)
        self.assertEqual(User.objects.count(), 1)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertFalse(user_created)

    def test_create_user_invalid_email(self):
        """It's impossible to create an user with invalid email
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        data = self.create_user_payload(email='invalid_email')
        res = self.api_create(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertEqual(User.objects.count(), 1)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertFalse(user_created)

    def test_create_user_existing_email(self):
        """It's impossible to create an user with an existing email
        """

        self.create_user(email='pre_existing_email@test.com')
        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 2)

        data = self.create_user_payload(
            email='pre_existing_email@test.com')
        res = self.api_create(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_existing_username(self):
        """It's impossible to create an user with an existing username
        """

        self.create_user(username='pre_existing_username')
        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 2)

        data = self.create_user_payload(username='pre_existing_username')
        res = self.api_create(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', res.data)
        self.assertEqual(User.objects.count(), 2)


class UserUpdateAPITests(UserTestMixin,
                         APITestMixin,
                         TestCase):

    def setUp(self):
        super().setUp()
        self.partial_update_view = 'core:user-retrieve-update'

    def test_update_user_valid_data(self):
        """It's possible to update an user with valid data
        """

        self.user = self.create_user(username='valid_username')
        self.assertEqual(self.user.username, 'valid_username')

        self.authenticate()
        data = {'username': 'new_valid_username'}
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_valid_username')

    def test_update_user_profile_valid_data(self):
        """It's possible to update an user profile data with valid data
        """

        self.user = self.create_user(given_name=None,
                                     family_name=None)
        self.assertEqual(self.user.profile.given_name, None)
        self.assertEqual(self.user.profile.family_name, None)

        self.authenticate()
        data = {'given_name': 'Ramon', 'family_name': 'Kayo'}
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.given_name, 'Ramon')
        self.assertEqual(self.user.profile.family_name, 'Kayo')

    def test_update_user_password_directly(self):
        """It's impossible to update user password directly
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate()

        data = {'password': 'NEW#valid_pass!123'}
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('NEW#valid_pass!123'))
        self.assertTrue(self.user.check_password('OLD#valid_pass!123'))

    def test_update_user_invalid_password(self):
        """It's impossible to update user password with invalid data
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate()

        data = {
            'password_1': 'NEW#valid_pass!123',
            'password_2': 'NEW#invalid_pass!123'
        }
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('NEW#valid_pass!123'))
        self.assertFalse(self.user.check_password('NEW#invalid_pass!123'))
        self.assertTrue(self.user.check_password('OLD#valid_pass!123'))

    def test_update_user_missing_password(self):
        """It's impossible to update user password without confirmation
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate()

        data = {'password_1': 'NEW#valid_pass!123'}
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('NEW#valid_pass!123'))
        self.assertTrue(self.user.check_password('OLD#valid_pass!123'))

    def test_update_user_valid_password(self):
        """It's possible to update user password with valid data
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate()

        data = {
            'password_1': 'NEW#valid_pass!123',
            'password_2': 'NEW#valid_pass!123'
        }
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NEW#valid_pass!123'))

    def test_update_user_email_directly(self):
        """It's impossible to update user email directly
        """

        initial_email = 'valid_email@test.com'
        new_email = 'new_valid_email@test.com'

        self.user = self.create_user(email=initial_email)
        self.authenticate()

        data = {'email': new_email}
        res = self.api_partial_update(data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, initial_email)


class UserResetPasswordAPITests(UserTestMixin,
                                APITestMixin,
                                TestCase):

    def setUp(self):
        super().setUp()
        self.password_recovery_view = 'core:user-password-recovery'
        self.password_reset_view = 'core:user-password-reset'

    def api_recover_password(self, **kwargs):
        return self.api_post(
            view_name=self.password_recovery_view,
            **kwargs
        )

    def api_reset_password(self, **kwargs):
        return self.api_patch(
            view_name=self.password_reset_view,
            **kwargs
        )

    def ask_password_reset(self):
        self.user = self.create_user(email='valid.email@test.com',
                                     password='OLD#pass!123')

        self.assertIsNone(self.user.reset_token)
        self.assertIsNone(self.user.reset_token_date)

        res = self.api_recover_password(data={'email': self.user.email})
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.reset_token)
        self.assertIsNotNone(self.user.reset_token_date)

    def test_update_password_valid_code_within_24h(self):
        """It's possible to reset user password with a valid code within 24h
        """

        self.ask_password_reset()

        now = timezone.now()
        self.user.reset_token_date = now - timezone.timedelta(
            hours=23)
        self.user.save()

        new_password = 'NEW#pass!123'

        res = self.api_reset_password(url_args=[self.user.pk],
                                      data={'reset_token': self.user.reset_token,
                                            'password_1': new_password,
                                            'password_2': new_password})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertIsNone(self.user.reset_token)
        self.assertIsNone(self.user.reset_token_date)
        self.assertTrue(self.user.check_password(new_password))

    def test_update_password_valid_code_after_24h(self):
        """It's impossible to reset user password with a valid code after 24h
        """

        self.ask_password_reset()

        now = timezone.now()
        self.user.reset_token_date = now - timezone.timedelta(
            hours=25)
        self.user.save()

        new_password = 'NEW#pass!123'

        res = self.api_reset_password(url_args=[self.user.pk],
                                      data={'reset_token': self.user.reset_token,
                                            'password_1': new_password,
                                            'password_2': new_password})

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('reset_token', res.data)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.reset_token)
        self.assertIsNotNone(self.user.reset_token_date)
        self.assertFalse(self.user.check_password(new_password))

    def test_update_password_invalid_code(self):
        """It's impossible to reset user password with an invalid code
        """

        self.ask_password_reset()

        new_password = 'NEW#pass!123'

        res = self.api_reset_password(url_args=[self.user.pk],
                                      data={'reset_token': 'INVALID',
                                            'password_1': new_password,
                                            'password_2': new_password})

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('reset_token', res.data)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.reset_token)
        self.assertIsNotNone(self.user.reset_token_date)
        self.assertFalse(self.user.check_password(new_password))

    def test_update_password_invalid_password(self):
        """It's impossible to reset user password with an invalid password
        """

        self.ask_password_reset()

        new_password_1 = 'NEW#pass!123'
        new_password_2 = 'INVALID#pass!456'

        res = self.api_reset_password(url_args=[self.user.pk],
                                      data={'reset_token': self.user.reset_token,
                                            'password_1': new_password_1,
                                            'password_2': new_password_2})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_2', res.data)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.reset_token)
        self.assertIsNotNone(self.user.reset_token_date)
        self.assertFalse(self.user.check_password(new_password_1))
        self.assertFalse(self.user.check_password(new_password_2))
