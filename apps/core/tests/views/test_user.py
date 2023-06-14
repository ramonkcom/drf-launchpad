from django.urls import reverse
from rest_framework import status
from django.test import TestCase

from ...models import User
from ..mixins import UserApiTestMixin


class UserApiCreateTests(UserApiTestMixin,
                         TestCase):

    def test_create_user_valid_data(self):
        """It's possible to create a user with valid data
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        url = reverse('core:user-create')
        data = self.create_user_payload()
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertTrue(user_created)

    def test_create_user_invalid_password(self):
        """It's impossible to create an user with invalid password
        """

        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 1)

        url = reverse('core:user-create')
        data = self.create_user_payload(
            password_2='different#pass!456',
        )
        res = self.api_client.post(url, data, format='json')

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

        url = reverse('core:user-create')
        data = self.create_user_payload(email='invalid_email')
        res = self.api_client.post(url, data, format='json')

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

        url = reverse('core:user-create')
        data = self.create_user_payload(
            email='pre_existing_email@test.com')
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_existing_username(self):
        """It's impossible to create an user with an existing username
        """

        self.create_user(username='pre_existing_username')
        # NOTE: 'django-guardian' creates an anonymous user on startup
        self.assertEqual(User.objects.count(), 2)

        url = reverse('core:user-create')
        data = self.create_user_payload(username='pre_existing_username')
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', res.data)
        self.assertEqual(User.objects.count(), 2)


class UserApiUpdateTests(UserApiTestMixin,
                         TestCase):

    def test_update_user_valid_data(self):
        """It's possible to update an user with valid data
        """

        self.user = self.create_user(username='valid_username')
        self.assertEqual(self.user.username, 'valid_username')

        self.authenticate(self.user)
        url = reverse('core:user-retrieve-update')
        data = {'username': 'new_valid_username'}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_valid_username')

    def test_update_user_person_valid_data(self):
        """It's possible to update an user personal data with valid data
        """

        self.user = self.create_user()
        self.assertEqual(self.user.person.given_name, None)
        self.assertEqual(self.user.person.family_name, None)

        self.authenticate(self.user)
        url = reverse('core:user-retrieve-update')
        data = {'given_name': 'Ramon', 'family_name': 'Kayo'}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.person.given_name, 'Ramon')
        self.assertEqual(self.user.person.family_name, 'Kayo')

    def test_update_user_password_directly(self):
        """It's impossible to update user password directly
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate(self.user)

        url = reverse('core:user-retrieve-update')
        data = {'password': 'NEW#valid_pass!123'}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OLD#valid_pass!123'))

    def test_update_user_invalid_password(self):
        """It's impossible to update user password with invalid data
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate(self.user)

        url = reverse('core:user-retrieve-update')
        data = {
            'password_1': 'NEW#valid_pass!123',
            'password_2': 'NEW#invalid_pass!123'
        }
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OLD#valid_pass!123'))

    def test_update_user_missing_password(self):
        """It's impossible to update user password without confirmation
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate(self.user)

        url = reverse('core:user-retrieve-update')
        data = {'password_1': 'NEW#valid_pass!123'}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OLD#valid_pass!123'))

    def test_update_user_valid_password(self):
        """It's possible to update user password with valid data
        """

        self.user = self.create_user(password='OLD#valid_pass!123')
        self.authenticate(self.user)

        url = reverse('core:user-retrieve-update')
        data = {
            'password_1': 'NEW#valid_pass!123',
            'password_2': 'NEW#valid_pass!123'
        }
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NEW#valid_pass!123'))

    def test_update_user_email_directly(self):
        """It's impossible to update user email directly
        """

        initial_email = 'valid_email@test.com'
        new_email = 'new_valid_email@test.com'

        self.user = self.create_user(email=initial_email)
        self.authenticate(self.user)

        url = reverse('core:user-retrieve-update')
        data = {'email': new_email}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, initial_email)
