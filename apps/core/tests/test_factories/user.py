from django.test import TestCase

from ...models import User


class UserFactoryTests(TestCase):

    def test_build_create_build_dict(self):
        """`UserFactory` builds and creates `User` objects consistently
        """

        def assert_roles(user):
            if type(user) is dict:
                self.assertTrue(user['is_active'])
                self.assertFalse(user['is_staff'])
                self.assertFalse(user['is_superuser'])

            else:
                self.assertTrue(user.is_active)
                self.assertFalse(user.is_staff)
                self.assertFalse(user.is_superuser)

        def assert_personal_data(user):
            if type(user) is dict:
                self.assertIsNotNone(user['given_name'])
                self.assertIsNotNone(user['family_name'])

            else:
                self.assertIsNotNone(user.person)
                self.assertIsNotNone(user.given_name)
                self.assertEqual(user.given_name, user.person.given_name)
                self.assertIsNotNone(user.family_name)
                self.assertEqual(user.family_name, user.person.family_name)

        def assert_username(user):
            if type(user) is dict:
                self.assertIsNotNone(user['username'])
                self.assertIn(user['given_name'].lower(), user['username'])
                self.assertIn(user['family_name'].lower(), user['username'])

            else:
                self.assertIsNotNone(user.username)
                self.assertIn(user.given_name.lower(), user.username)
                self.assertIn(user.family_name.lower(), user.username)

        def assert_email(user):
            email_regex = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
            if type(user) is dict:
                self.assertIsNotNone(user['email'])
                self.assertIn(user['username'], user['email'])
                self.assertRegex(user['email'], email_regex)

            else:
                self.assertIsNotNone(user.email)
                self.assertIn(user.username, user.email)
                self.assertRegex(user.email, email_regex)

        user_dict = User.factory.build_dict()

        self.assertIsInstance(user_dict, dict)
        assert_roles(user_dict)
        assert_personal_data(user_dict)
        assert_username(user_dict)
        assert_email(user_dict)

        built_user = User.factory.build()

        self.assertIsInstance(built_user, User)
        assert_roles(built_user)
        assert_personal_data(built_user)
        assert_username(built_user)
        assert_email(built_user)

        self.assertFalse(built_user.emails.exists())

        created_user = User.factory.create()

        self.assertIsInstance(created_user, User)
        assert_roles(created_user)
        assert_personal_data(created_user)
        assert_username(created_user)
        assert_email(created_user)

        self.assertTrue(created_user.emails.exists())
        self.assertEqual(created_user.emails.count(), 1)

    def test_build_allows_customization(self):
        """`UserFactory` allows building customized `User` objects
        """

        user = User.factory.build(
            is_active=False,
            is_staff=True,
            is_superuser=True,
            given_name='Ramon',
            family_name='Kayo',
            username='ramon_kayo',
            email='ramon@test.com',
        )

        self.assertIsInstance(user, User)
        self.assertFalse(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.given_name, 'Ramon')
        self.assertEqual(user.person.given_name, 'Ramon')
        self.assertEqual(user.family_name, 'Kayo')
        self.assertEqual(user.person.family_name, 'Kayo')
        self.assertEqual(user.username, 'ramon_kayo')
        self.assertEqual(user.email, 'ramon@test.com')

    def test_create_allows_customization(self):
        """`UserFactory` allows creating customized `User` objects
        """

        user = User.factory.create(
            is_active=False,
            is_staff=True,
            is_superuser=True,
            given_name='Ramon',
            family_name='Kayo',
            username='ramon_kayo',
            email='ramon@test.com',
        )

        self.assertIsInstance(user, User)
        self.assertFalse(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.given_name, 'Ramon')
        self.assertEqual(user.person.given_name, 'Ramon')
        self.assertEqual(user.family_name, 'Kayo')
        self.assertEqual(user.person.family_name, 'Kayo')
        self.assertEqual(user.username, 'ramon_kayo')
        self.assertEqual(user.email, 'ramon@test.com')

        self.assertTrue(user.emails.exists())
        self.assertEqual(user.emails.count(), 1)
        self.assertEqual(user.emails.first().address, user.email)

    def test_build_dict_allows_customization(self):
        """`UserFactory` allows building customized `User` dicts
        """

        user_dict = User.factory.build_dict(
            is_active=False,
            is_staff=True,
            is_superuser=True,
            given_name='Ramon',
            family_name='Kayo',
            username='ramon_kayo',
            email='ramon@test.com',
            unknown_field='TEST',
        )

        self.assertIsInstance(user_dict, dict)
        self.assertFalse(user_dict['is_active'])
        self.assertTrue(user_dict['is_staff'])
        self.assertTrue(user_dict['is_superuser'])
        self.assertEqual(user_dict['given_name'], 'Ramon')
        self.assertEqual(user_dict['family_name'], 'Kayo')
        self.assertEqual(user_dict['username'], 'ramon_kayo')
        self.assertEqual(user_dict['email'], 'ramon@test.com')

        self.assertIn('unknown_field', user_dict)
        self.assertEqual(user_dict['unknown_field'], 'TEST')

        self.assertNotIn('id', user_dict)
        self.assertNotIn('date_joined', user_dict)
        self.assertNotIn('groups', user_dict)
        self.assertNotIn('user_permissions', user_dict)
        # NOTE This is `Person` FK to `User`
        self.assertNotIn('user', user_dict)
        self.assertIn('password', user_dict)

        exclusive_dict = User.factory.build_dict(
            username='tester',
            exclude_fields=[
                'given_name',
                'family_name',
                'password_1',
                'password_2',
                'is_active',
                'is_staff',
                'is_superuser',
            ],
        )

        self.assertIsInstance(exclusive_dict, dict)

        self.assertIn('username', exclusive_dict)
        self.assertEqual(exclusive_dict['username'], 'tester')

        self.assertIn('email', exclusive_dict)

        self.assertNotIn('given_name', exclusive_dict)
        self.assertNotIn('family_name', exclusive_dict)
        self.assertNotIn('password_1', exclusive_dict)
        self.assertNotIn('password_2', exclusive_dict)
        self.assertNotIn('is_active', exclusive_dict)
        self.assertNotIn('is_staff', exclusive_dict)
        self.assertNotIn('is_superuser', exclusive_dict)

        inclusive_dict = User.factory.build_dict(
            username='tester',
            include_fields=[
                'given_name',
                'username',
            ],
        )

        self.assertIsInstance(inclusive_dict, dict)

        self.assertEqual(len(inclusive_dict), 2)
        self.assertIn('given_name', inclusive_dict)
        self.assertIn('username', inclusive_dict)
