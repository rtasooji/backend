from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test the user created successfully
        :return:
        """
        payload = {
            'email': 'test@test.com',
            'password': 'userPass',
            'name': "test test"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_password_length(self):
        """
        Test the length of the password is greater than 5 characters
        :return:
        """
        payload = {
            'email': 'test@test.com',
            'password': '1234',
            'name': 'test test'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # check it is not created
        user_exist = get_user_model().objects.filter(email=payload['email']
                                                     ).exists()
        self.assertFalse(user_exist)

    def test_duplicate_user(self):
        """
        Test duplicate users inside model
        :return:
        """
        payload = {
            'email': 'test@test.com',
            'password': "userPass",
            'name': "test test"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# testing tokens

    def test_create_token_for_user(self):
        """
        Test the token is created successfully
        :return:
        """
        payload = {
            'email': 'test@test.com',
            'password': 'userPass',
            'name': 'test test'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credential(self):
        create_user(email="test@test.com", password="userPass")
        payload = {'email': 'test@test.com', 'password': 'wrongPass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_create_user(self):
        payload = {'email': 'test@test.com',
                   'password': 'userPass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_without_password(self):
        payload = {'email': 'test@test.com',
                   'password': 'userPass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, {'email': 'test@test.com',
                                           'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthenticated(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):

    def setUp(self):
        self.user = create_user(email="test@test.com", password="userPass",
                                name="test test")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_successful(self):
        """
        Testing the profile of authenticated user is successfully retrieved
        :return:
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name,
                                    'email': self.user.email})

    def test_post_me_not_allowed(self):
        """
        Testing post request is not allowed
        :return:
        """
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Testing patching user profile works
        :return:
        """
        payload = {'name': 'new name',
                   'password': 'newPass'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
