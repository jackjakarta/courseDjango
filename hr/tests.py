from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from .views import home_view


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))  # Use the URL pattern name 'home' here
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        response = self.client.get(reverse('home'))  # Use the URL pattern name 'home' here
        self.assertTemplateUsed(response, 'home.html')  # Replace 'myapp/home.html' with your actual template path
