from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.super_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='1234'
        )
        self.client.force_login(self.super_user)
        self.user = get_user_model().objects.create_user(
            email='user@test.com',
            password='1234',
            name='test regular user'
        )

    def test_users_listed(self):
        """
        Test that users are listed on user page
        :return:
        """
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user edit page worksfieldset
        :return:
        """
        # generates a url /admin/core/user/id/change the id comes from args
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        """
        Test that the user can be added
        :return:
        """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
