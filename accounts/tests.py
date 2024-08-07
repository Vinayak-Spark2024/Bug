from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password123'
        )
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'phone_number': '1234567890',
            'name': 'New User'
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'user',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
    def test_logout_user(self):
        url = reverse('logout')
        refresh = RefreshToken.for_user(self.regular_user)
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'refresh': str(refresh)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_detail(self):
        url = reverse('user-detail', args=[self.regular_user.id])
        response = self.admin_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.regular_user.username)
        
    def test_user_list(self):
        url = reverse('user-list')
        response = self.admin_client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # At least admin and regular_user

    def test_register_user_as_regular_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser2',
            'password': 'newpassword123',
            'email': 'newuser2@example.com',
            'phone_number': '0987654321',
            'name': 'New User 2'
        }
        # Ensure the client is not authenticated
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_as_regular_user(self):
        url = reverse('user-detail', args=[self.regular_user.id])
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'phone_number': '0987654321',
            'name': 'Updated User'
        }
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
