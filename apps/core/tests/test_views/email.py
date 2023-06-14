import uuid

from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from django.utils import timezone

from ...models import Email
from ..mixins import UserAPITestsMixin


class EmailAPITests(UserAPITestsMixin,
                    TestCase):

    def test_confirm_user_email_invalid_code(self):
        """It's impossible to confirm user email with invalid code
        """

        self.user = self.create_user()
        email = self.user.primary_email
        self.assertIsNotNone(email)

        url = reverse('core:email-confirmation', args=[email.pk])
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

        url = reverse('core:email-confirmation', args=[email.pk])
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

        url = reverse('core:email-confirmation', args=[email.pk])
        data = {'confirmation_code': email.confirmation_code}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmation_code', res.data)

        email.refresh_from_db()
        self.assertFalse(email.is_confirmed)

    def test_add_user_email(self):
        """It's possible to add new email to user
        """

        self.user = self.create_user()
        self.authenticate(self.user)
        self.assertEqual(self.user.emails.count(), 1)

        url = reverse('core:email-create')
        data = {'address': 'new.valid.email@test.com'}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user.emails.count(), 2)

        new_email = self.user.emails.filter(address=data['address']).first()
        self.assertIsNotNone(new_email)
        self.assertFalse(new_email.is_primary)
        self.assertFalse(new_email.is_confirmed)

    def test_add_user_email_existing(self):
        """It's impossible to add an existing email to user
        """

        existing_email = 'other.user@test.com'
        self.create_user(email=existing_email)

        self.user = self.create_user()
        self.authenticate(self.user)
        self.assertEqual(self.user.emails.count(), 1)

        url = reverse('core:email-create')
        data = {'address': existing_email}
        res = self.api_client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('address', res.data)
        self.assertEqual(self.user.emails.count(), 1)

        existing_email_qs = self.user.emails.filter(address=existing_email)
        self.assertFalse(existing_email_qs.exists())

    def test_remove_user_additional_email(self):
        """It's possible to remove user additional emails
        """

        self.user = self.create_user(email='valid.email@test.com')
        self.authenticate(self.user)
        new_email = Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )
        self.assertEqual(self.user.emails.count(), 2)

        url = reverse('core:email-update-destroy', args=[new_email.pk])
        res = self.api_client.delete(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.emails.count(), 1)
        self.assertFalse(self.user.emails.filter(
            address='another.valid.email@test.com').exists())

    def test_remove_user_primary_email(self):
        """It's impossible to remove user primary email
        """

        self.user = self.create_user(email='valid.email@test.com')
        self.authenticate(self.user)
        Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )
        self.assertEqual(self.user.emails.count(), 2)

        primary_email = self.user.primary_email
        url = reverse('core:email-update-destroy', args=[primary_email.pk])
        res = self.api_client.delete(url, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data)
        self.assertEqual(self.user.emails.count(), 2)

    def test_make_user_confirmed_email_primary(self):
        """It's possible to make an confirmed email primary
        """

        self.user = self.create_user(email='valid.email@test.com')
        self.authenticate(self.user)
        additional_email = Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )

        additional_email.confirm()
        self.assertFalse(additional_email.is_primary)

        url = reverse('core:email-update-destroy', args=[additional_email.pk])
        data = {'is_primary': True}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        additional_email.refresh_from_db()
        self.user.refresh_from_db()

        self.assertTrue(additional_email.is_primary)
        self.assertEqual(self.user.email, additional_email.address)

    def test_make_user_unconfirmed_email_primary(self):
        """It's impossible to an unconfirmed email primary
        """

        initial_email = 'valid.email@test.com'
        self.user = self.create_user(email=initial_email)
        self.authenticate(self.user)
        additional_email = Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )

        self.assertFalse(additional_email.is_confirmed)
        self.assertFalse(additional_email.is_primary)

        url = reverse('core:email-update-destroy', args=[additional_email.pk])
        data = {'is_primary': True}
        res = self.api_client.patch(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data)

        additional_email.refresh_from_db()
        self.user.refresh_from_db()

        self.assertFalse(additional_email.is_primary)
        self.assertEqual(self.user.email, initial_email)
