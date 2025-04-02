from django.test import TestCase
from django.urls import reverse


class SimpleTest(TestCase):
    def test_test_home(self):
        response = self.client.get(reverse('test-home'))
        self.assertEqual(response.status_code, 200)