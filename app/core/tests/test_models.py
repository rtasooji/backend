from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with email and password
        """
        email = "test@test.com"
        password = "1234"
        # calling create user function from user manager for our user model
        # this will fail in test because we haven't costumized user model and
        #   it expect the standard username field, which is requird for
        #   django default user model, so we need to create our user model
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # because password in encrypted we can not check it with assertEqual
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the lower case domain name
        :return:
        """
        # for this to work we add self.normalize_email function in our
        # models.py in user manager
        email = "test@DOMAIN.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password='password'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalide_email(self):
        """
        Test creating email with no email
        :return:
        """
        # anything in here should raise ValueError
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password')

    def test_new_super_user(self):
        """
        Test creating super user
        :return:
        """
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'password')
        # super user variable is part of the PermissionMixin package
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
