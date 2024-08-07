# department/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Department

User = get_user_model()

class DepartmentTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpass'
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='userpass'
        )
        self.department_data = {
            'user': self.admin_user,  # Use the actual user instance
            'department': Department.PYTHON,
            'role': Department.DEVELOPER
        }
        self.client = APIClient()

    def test_create_department_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(reverse('department-list-create'), {
            'user': self.admin_user.id,  # Pass the user's ID for the request
            'department': self.department_data['department'],
            'role': self.department_data['role']
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().user, self.admin_user)

    def test_create_department_as_non_admin(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(reverse('department-list-create'), {
            'user': self.admin_user.id,  # Pass the user's ID for the request
            'department': self.department_data['department'],
            'role': self.department_data['role']
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_departments_as_admin(self):
        Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('department-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_departments_as_non_admin(self):
        Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('department-list-create'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_department_as_admin(self):
        department = Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('department-detail', kwargs={'pk': department.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], department.id)

    def test_retrieve_department_as_non_admin(self):
        department = Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('department-detail', kwargs={'pk': department.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_department_as_admin(self):
        department = Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.admin_user)
        updated_data = {
            'user': self.admin_user.id,  # Pass the user's ID for the request
            'department': Department.JAVA,
            'role': Department.TESTER
        }
        response = self.client.put(reverse('department-detail', kwargs={'pk': department.pk}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        department.refresh_from_db()
        self.assertEqual(department.department, Department.JAVA)
        self.assertEqual(department.role, Department.TESTER)

    def test_update_department_as_non_admin(self):
        department = Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.regular_user)
        updated_data = {
            'user': self.admin_user.id,  # Pass the user's ID for the request
            'department': Department.JAVA,
            'role': Department.TESTER
        }
        response = self.client.put(reverse('department-detail', kwargs={'pk': department.pk}), updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_department_as_admin(self):
        department = Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(reverse('department-detail', kwargs={'pk': department.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)

    def test_delete_department_as_non_admin(self):
        department = Department.objects.create(**self.department_data)
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(reverse('department-detail', kwargs={'pk': department.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Department.objects.count(), 1)