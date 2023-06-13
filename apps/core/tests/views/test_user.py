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

