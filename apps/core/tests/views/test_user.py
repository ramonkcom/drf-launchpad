import uuid

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from django.utils import timezone
from django.utils.http import urlencode

from ...models import User
from ..mixins import UserApiTestMixin


class UserApiCreateTests(UserApiTestMixin,
                         TestCase):

    def test_create_user_valid_data(self):
        """It's possible to create a user with valid data
        """

        self.assertEqual(User.objects.count(), 0)

        url = reverse('core:user-create')
        data = self.create_user_payload()
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertTrue(user_created)

    def test_create_user_invalid_password(self):
        """It's impossible to create an user with invalid password
        """

        self.assertEqual(User.objects.count(), 0)

        url = reverse('core:user-create')
        data = self.create_user_payload(
            password_2='different#pass!456',
        )
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_2', res.data)
        self.assertEqual(User.objects.count(), 0)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertFalse(user_created)

    def test_create_user_invalid_email(self):
        """It's impossible to create an user with invalid email
        """

        self.assertEqual(User.objects.count(), 0)

        url = reverse('core:user-create')
        data = self.create_user_payload(email='invalid_email')
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertEqual(User.objects.count(), 0)

        user_created = User.objects.filter(email=data['email']).exists()
        self.assertFalse(user_created)

    def test_create_user_existing_email(self):
        """It's impossible to create an user with an existing email
        """

        self.create_user(email='pre_existing_email@test.com')
        self.assertEqual(User.objects.count(), 1)

        url = reverse('core:user-create')
        data = self.create_user_payload(
            email='pre_existing_email@test.com')
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_existing_username(self):
        """It's impossible to create an user with an existing username
        """

        self.create_user(username='pre_existing_username')
        self.assertEqual(User.objects.count(), 1)

        url = reverse('core:user-create')
        data = self.create_user_payload(username='pre_existing_username')
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', res.data)
        self.assertEqual(User.objects.count(), 1)

    def test_confirm_user_email_invalid_code(self):
        """It's impossible to confirm user email with invalid code
        """

        self.user = self.create_user()
        email = self.user.emails.filter(address=self.user.email).first()
        self.assertIsNotNone(email)

        url = reverse('core:email-confirm', args=[email.pk])
        data = {'confirmation_code': uuid.uuid4()}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        email.refresh_from_db()
        self.assertFalse(email.is_confirmed)

    def test_confirm_user_email_within_24h(self):
        """It's possible to confirm user email within 24 hours
        """

        self.user = self.create_user()
        email = self.user.emails.filter(address=self.user.email).first()
        self.assertIsNotNone(email)

        now = timezone.now()
        email.confirmation_code_date = now - timezone.timedelta(
            hours=23)
        email.save()

        url = reverse('core:email-confirm', args=[email.pk])
        data = {'confirmation_code': email.confirmation_code}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        email.refresh_from_db()
        self.assertTrue(email.is_confirmed)

    def test_confirm_user_email_after_24h(self):
        """It's impossible to confirm user email after 24 hours
        """

        self.user = self.create_user()
        email = self.user.emails.filter(address=self.user.email).first()
        self.assertIsNotNone(email)

        email.confirmation_code_date = timezone.now() - timezone.timedelta(
            hours=25)
        email.save()

        url = reverse('core:email-confirm', args=[email.pk])
        data = {'code': email.confirmation_code}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmation_code', res.data)

        email.refresh_from_db()
        self.assertFalse(email.is_confirmed)
