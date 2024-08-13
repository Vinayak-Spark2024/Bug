from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create 10 users for testing
        self.users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password='password123',
                role='developer',
                dept='python'
            )
            self.users.append(user)
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123',
            role='manager',
            dept='management',
            is_staff=True
        )
        
        self.client.force_authenticate(user=self.admin_user)
        
        # JWT Tokens
        self.refresh = RefreshToken.for_user(self.admin_user)
        self.access_token = str(self.refresh.access_token)
        self.refresh_token = str(self.refresh)
    
    def test_register_user(self):
        response = self.client.post('/api/accounts/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'role': 'developer',
            'dept': 'python'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_login_user(self):
        response = self.client.post('/api/accounts/login/', {
            'email': 'user0@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_logout_user(self):
        response = self.client.post('/api/accounts/logout/', {
            'refresh': self.refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
    
    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/api/accounts/profile/{self.users[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.patch(f'/api/accounts/profile/{self.users[0].id}/', {
            'dept': 'java'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dept'], 'java')
    
    def test_delete_user_profile(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.delete(f'/api/accounts/profile/{self.users[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_get_all_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)  # 10 users + admin
    
    def test_get_all_users_as_non_admin(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_login_invalid_credentials(self):
        response = self.client.post('/api/accounts/login/', {
            'email': 'user0@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout_invalid_token(self):
        response = self.client.post('/api/accounts/logout/', {
            'refresh': 'invalidtoken'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_user_profile_without_permission(self):
        self.client.force_authenticate(user=self.users[1])
        response = self.client.patch(f'/api/accounts/profile/{self.users[0].id}/', {
            'dept': 'java'
        })
        print("\n",response.data,"\n")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_nonexistent_user_profile(self):
        response = self.client.get('/api/accounts/profile/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_user_profile(self):
        response = self.client.delete('/api/accounts/profile/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_register_user_missing_field(self):
        response = self.client.post('/api/accounts/register/', {
            'username': 'incompleteuser',
            'email': 'incompleteuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_user_profile_invalid_field(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.patch(f'/api/accounts/profile/{self.users[0].id}/', {
            'invalid_field': 'value'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_with_username(self):
        response = self.client.post('/api/accounts/login/', {
            'email': 'user0@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # Additional edge cases
    def test_login_with_missing_email(self):
        response = self.client.post('/api/accounts/login/', {
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_with_missing_password(self):
        response = self.client.post('/api/accounts/login/', {
            'email': 'user0@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_with_existing_email(self):
        response = self.client.post('/api/accounts/register/', {
            'username': 'anotheruser',
            'email': 'user0@example.com',
            'password': 'password123',
            'role': 'developer',
            'dept': 'python'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout_without_token(self):
        response = self.client.post('/api/accounts/logout/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_own_profile(self):
        self.client.force_authenticate(user=self.users[1])
        response = self.client.patch(f'/api/accounts/profile/{self.users[1].id}/', {
            'dept': 'angular'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dept'], 'angular')
    
    def test_get_user_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/accounts/profile/{self.users[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_user_list(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)  # 10 users + admin
    
    def test_non_admin_user_list(self):
        self.client.force_authenticate(user=self.users[1])
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_user_profile_with_permissions(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/accounts/profile/{self.users[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_profile_update_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(f'/api/accounts/profile/{self.users[1].id}/', {
            'dept': 'devops'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['dept'], 'devops')
    
    def test_user_profile_delete_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/accounts/profile/{self.users[1].id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_user_list_view_as_manager(self):
        manager_user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='password123',
            role='manager',
            dept='management',
            is_staff=True
        )
        self.client.force_authenticate(user=manager_user)
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_list_view_as_team_lead(self):
        team_lead_user = User.objects.create_user(
            username='teamlead',
            email='teamlead@example.com',
            password='password123',
            role='team_lead',
            dept='python',
            is_staff=True
        )
        self.client.force_authenticate(user=team_lead_user)
        response = self.client.get('/api/accounts/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_profile_update_as_team_lead(self):
        team_lead_user = User.objects.create_user(
            username='teamlead',
            email='teamlead@example.com',
            password='password123',
            role='team_lead',
            dept='python',
            is_staff=True
        )
        self.client.force_authenticate(user=team_lead_user)
        response = self.client.patch(f'/api/accounts/profile/{self.users[1].id}/', {
            'dept': 'java'
        })
        print("\n",response.data,"\n")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
