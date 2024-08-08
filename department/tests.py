from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Department

User = get_user_model()

class DepartmentTests(APITestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.normal_user = User.objects.create_user(username='user', password='userpass')
        
        # Create JWT tokens
        self.admin_token = self.get_jwt_token(self.admin_user)
        self.normal_user_token = self.get_jwt_token(self.normal_user)

        # Ensure no existing department for the admin user
        Department.objects.filter(user=self.admin_user).delete()
        
        # Create a Department instance for normal user
        self.department = Department.objects.create(
            user=self.normal_user,
            role='manager',
            dept='python'
        )
        
        # Define URLs
        self.list_url = reverse('department-list-create')
        self.detail_url = reverse('department-detail', kwargs={'pk': self.department.pk})

    def get_jwt_token(self, user):
        """ Helper function to get JWT token """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_admin_can_list_departments(self):
        """ Test that admin user can list departments """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_cannot_list_departments(self):
        """ Test that normal user cannot list departments """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.normal_user_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_department(self):
        """ Test that admin user can create a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            'user': self.normal_user.id,  # Ensure this is the correct field type
            'role': 'developer',         # Ensure this is one of the allowed choices
            'dept': 'java'               # Ensure this is one of the allowed choices
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update_department(self):
        """ Test that admin user can update a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            'user': self.normal_user.id,  # Ensure this is the correct field type
            'role': 'tester',             # Ensure this is one of the allowed choices
            'dept': 'devops'              # Ensure this is one of the allowed choices
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_normal_user_cannot_create_department(self):
        """ Test that normal user cannot create a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.normal_user_token)
        data = {
            'user': self.normal_user.id,
            'role': 'customer',
            'dept': 'management'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_department(self):
        """ Test that admin user can retrieve a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_normal_user_cannot_retrieve_department(self):
        """ Test that normal user cannot retrieve a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.normal_user_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_normal_user_cannot_update_department(self):
        """ Test that normal user cannot update a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.normal_user_token)
        data = {
            'role': 'tester',
            'dept': 'devops'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_department(self):
        """ Test that admin user can delete a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)

    def test_normal_user_cannot_delete_department(self):
        """ Test that normal user cannot delete a department """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.normal_user_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
