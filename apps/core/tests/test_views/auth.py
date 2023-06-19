from django.test import TestCase
from rest_framework import status

from apps.utils.tests.mixins import APITestMixin

from ..mixins import UserTestMixin


class AuthenticationAPITests(UserTestMixin,
                             APITestMixin,
                             TestCase):

    def setUp(self):
        super().setUp()
        self.obtain_token_view = 'core:auth'

    def api_authenticate(self, **kwargs):
        return self.api_post(self.obtain_token_view, **kwargs)

    def test_obtain_token_email_not_confirmed(self):
        """It's impossible to obtain a token for an user before confirming email
        """

        password = 'valid#pass!123'

        self.user = self.create_user(
            email='not_confirmed@test.com',
            password=password,
        )

        data = {
            'email': self.user.email,
            'password': password,
        }
        res = self.api_authenticate(data=data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('refresh', res.data)
        self.assertNotIn('access', res.data)
        self.assertIn('email', res.data)

    def test_obtain_token_email_confirmed(self):
        """It's impossible to obtain a token for an user before confirming email
        """

        password = 'valid#pass!123'

        self.user = self.create_user(password=password)
        email = self.user.primary_email
        self.assertIsNotNone(email)
        email.confirm()

        data = {
            'email': self.user.email,
            'password': password,
        }
        res = self.api_authenticate(data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
