from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from ..mixins import UserAPITestsMixin


class TokenAPITests(UserAPITestsMixin,
                    TestCase):

    def test_obtain_token_email_not_confirmed(self):
        """It's impossible to obtain a token for an user before confirming email
        """

        password = 'valid#pass!123'

        self.user = self.create_user(
            email='not_confirmed@test.com',
            password=password,
        )

        url = reverse('core:token-obtain')
        data = {
            'email': self.user.email,
            'password': password,
        }
        res = self.api_client.post(url, data, format='json')

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

        url = reverse('core:token-obtain')
        data = {
            'email': self.user.email,
            'password': password,
        }
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
