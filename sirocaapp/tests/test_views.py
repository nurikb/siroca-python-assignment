from django.test import TestCase, Client
from django.urls import reverse
from sirocaapp.models import UserRequest, UserRequestResult


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('git_url')

    def test_get_request(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviroapp/index.html')

    def test_post_request_pulls(self):
        response = self.client.post(self.url, {
            'url': 'https://github.com/django/asgiref'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTrue('pulls' in response.context)

    def test_post_request_without_pulls(self):
        response = self.client.post(self.url, {
            'url': 'https://github.com/nurikb/inventory'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTrue('empty' in response.context)

    def test_post_invalid_request(self):
        response = self.client.post(self.url, {
            'url': 'github.com/django/asgiref'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTrue('form' in response.context)