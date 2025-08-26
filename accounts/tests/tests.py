from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import CustomUser, Profile

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="farmer1", email="farmer@example.com", password="password123", role="farmer", location="Lagos")
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')

    def authenticate(self):
        response = self.client.post(self.login_url, {'username': 'farmer1', 'password': 'password123'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_profile_auto_created(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_retrieve_profile(self):
        self.authenticate()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('phone_number', response.data)

    def test_update_profile(self):
        self.authenticate()
        response = self.client.patch(self.profile_url, {'phone_number': '08012345678'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '08012345678')
        self.assertEqual(response.data['bio'], '')
        self.assertEqual(response.data['avatar'], None)
