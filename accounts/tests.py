from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import User

class AuthTests(APITestCase):
    def test_user_registration_and_login(self):
        # Register a user
        register_url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'farmer',
            'location': 'Lagos'
        }
        response = self.client.post(register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['role'], 'farmer')
        self.assertEqual(response.data['user']['location'], 'Lagos')

        # Login the same user
        login_url = reverse('login')
        login_data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

