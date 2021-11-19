from http import HTTPStatus
from urllib.parse import urlparse, parse_qsl
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse, resolve

from catalog.models import Category
from .fixtures.categories import TEST_CATEGORY

User = get_user_model()

TEST_USER = {
    'email': 'test@test.com',
    'password': '1234'
}


class TestCategoryView(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        user_obj = User.objects.create(email=TEST_USER['email'])
        user_obj.set_password(TEST_USER['password'])
        user_obj.save()
        cls.user = user_obj

        cls.client = Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = 'catalog:one_cat'

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_category_view_redirect(self):
        url = reverse(
            self.base_url,
            kwargs={
                'category_slug': 'test'
            }
        )

        response = self.client.get(url, follow=True)

        parsed_url = urlparse(response.url)
        query_dict: dict = dict(parse_qsl(parsed_url.query))
        redirect_url = resolve(parsed_url.path)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(redirect_url.view_name, 'authentication:login')
        self.assertEqual(query_dict['next'], url)

    def test_category_view_not_found(self):
        self.client.login(email=self.user.email, password=TEST_USER['password'])
        url = reverse(
            self.base_url,
            kwargs={
                'category_slug': 'test'
            }
        )

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    '''def test_category_view_okay(self):
        self.client.login(email=self.user.email, password=TEST_USER['password'])

        Category.objects.create(**TEST_CATEGORY)

        url = reverse(
            self.base_url,
            kwargs={
                'category_slug':TEST_CATEGORY['slug']
            }
        )

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code,HTTPStatus.OK)
        self.assertEqual(response.templates[0].name, 'catalog/one_categories.html')
        self.assertEqual(response.context['category'].slug, TEST_CATEGORY['slug'])'''

    @patch('catalog.views.get_category', return_value=Mock())
    def test_category_view_okay(self, mock_get_category):
        category = Category(**TEST_CATEGORY)

        mock_get_category.returt_value = category
        self.client.login(email=self.user.email, password=TEST_USER['password'])

        url = reverse(
            self.base_url,
            kwargs={
                'category_slug': TEST_CATEGORY['slug']
            }
        )

        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.templates[0].name, 'catalog/one_categories.html')
        self.assertEqual(response.context['category'].slug, TEST_CATEGORY['slug'])
        mock_get_category.assert_called_once_with (TEST_CATEGORY['slug'])
