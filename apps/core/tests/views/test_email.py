import uuid

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from django.utils import timezone

from ...models import Email
from ..mixins import UserApiTestMixin


class EmailApiTests(UserApiTestMixin,
                    TestCase):

    def test_confirm_user_email_invalid_code(self):
        """It's impossible to confirm user email with invalid code
        """

        self.user = self.create_user()
        email = self.user.primary_email
        self.assertIsNotNone(email)

        url = reverse('core:email-confirmation', args=[self.user.pk, email.pk])
        data = {'confirmation_code': uuid.uuid4()}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmation_code', res.data)

        email.refresh_from_db()
        self.assertFalse(email.is_confirmed)

    def test_confirm_user_email_within_24h(self):
        """It's possible to confirm user email within 24 hours
        """

        self.user = self.create_user()
        email = self.user.primary_email
        self.assertIsNotNone(email)

        now = timezone.now()
        email.confirmation_code_date = now - timezone.timedelta(
            hours=23)
        email.save()

        url = reverse('core:email-confirmation', args=[self.user.pk, email.pk])
        data = {'confirmation_code': email.confirmation_code}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        email.refresh_from_db()
        self.assertTrue(email.is_confirmed)

    def test_confirm_user_email_after_24h(self):
        """It's impossible to confirm user email after 24 hours
        """

        self.user = self.create_user()
        email = self.user.primary_email
        self.assertIsNotNone(email)

        email.confirmation_code_date = timezone.now() - timezone.timedelta(
            hours=25)
        email.save()

        url = reverse('core:email-confirmation', args=[self.user.pk, email.pk])
        data = {'confirmation_code': email.confirmation_code}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmation_code', res.data)

        email.refresh_from_db()
        self.assertFalse(email.is_confirmed)
