import uuid

from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from apps.utils.tests.mixins import APITestMixin

from ..mixins import UserTestMixin
from ...models import Email


class EmailAPITests(UserTestMixin,
                    APITestMixin,
                    TestCase):

    def setUp(self):
        super().setUp()
        self.confirm_view = 'core:email-confirmation'
        self.create_view = 'core:email-create'
        self.destroy_view = 'core:email-update-destroy'
        self.partial_update_view = 'core:email-update-destroy'

    def api_confirm(self, **kwargs):
        return self.api_post(self.confirm_view, **kwargs)

    def test_confirm_user_email_invalid_code(self):
        """It's impossible to confirm user email with invalid code
        """

        self.user = self.create_user()
        email = self.user.primary_email
        self.assertIsNotNone(email)

        data = {'confirmation_code': uuid.uuid4()}
        res = self.api_confirm(url_args=[email.pk], data=data)

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

        data = {'confirmation_code': email.confirmation_code}
        res = self.api_confirm(url_args=[email.pk], data=data)

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

        data = {'confirmation_code': email.confirmation_code}
        res = self.api_confirm(url_args=[email.pk], data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmation_code', res.data)

        email.refresh_from_db()
        self.assertFalse(email.is_confirmed)

    def test_add_user_email(self):
        """It's possible to add new email to user
        """

        self.user = self.create_user()
        self.authenticate()
        self.assertEqual(self.user.emails.count(), 1)

        data = {'address': 'new.valid.email@test.com'}
        res = self.api_create(data=data)

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
        self.authenticate()
        self.assertEqual(self.user.emails.count(), 1)

        data = {'address': existing_email}
        res = self.api_create(data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('address', res.data)
        self.assertEqual(self.user.emails.count(), 1)

        existing_email_qs = self.user.emails.filter(address=existing_email)
        self.assertFalse(existing_email_qs.exists())

    def test_remove_user_additional_email(self):
        """It's possible to remove user additional emails
        """

        self.user = self.create_user(email='valid.email@test.com')
        self.authenticate()
        new_email = Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )
        self.assertEqual(self.user.emails.count(), 2)

        res = self.api_destroy(url_args=[new_email.pk])

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.user.emails.count(), 1)
        self.assertFalse(self.user.emails.filter(
            address='another.valid.email@test.com').exists())

    def test_remove_user_primary_email(self):
        """It's impossible to remove user primary email
        """

        self.user = self.create_user(email='valid.email@test.com')
        self.authenticate()
        Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )
        self.assertEqual(self.user.emails.count(), 2)

        res = self.api_destroy(url_args=[self.user.primary_email.pk])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data)
        self.assertEqual(self.user.emails.count(), 2)

    def test_make_user_confirmed_email_primary(self):
        """It's possible to make an confirmed email primary
        """

        self.user = self.create_user(email='valid.email@test.com')
        self.authenticate()
        additional_email = Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )

        additional_email.confirm()
        self.assertFalse(additional_email.is_primary)

        data = {'is_primary': True}
        res = self.api_partial_update(
            url_args=[additional_email.pk], data=data)

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
        self.authenticate()
        additional_email = Email.objects.create(
            address='another.valid.email@test.com',
            user=self.user,
        )

        self.assertFalse(additional_email.is_confirmed)
        self.assertFalse(additional_email.is_primary)

        data = {'is_primary': True}
        res = self.api_partial_update(
            url_args=[additional_email.pk], data=data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data)

        additional_email.refresh_from_db()
        self.user.refresh_from_db()

        self.assertFalse(additional_email.is_primary)
        self.assertEqual(self.user.email, initial_email)
