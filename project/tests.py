from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Project, ProjectUser
from department.models import Department
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectTests(TestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='user', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='password')

        # Create departments
        self.dept_python = Department.objects.create(user=self.user, role='developer', dept='python')

        # Create projects
        self.project = Project.objects.create(
            project_name='Project X',
            project_duration=30,
            client_name='Client A',
            submission_date='2024-08-01'
        )

        # Create project-user assignments
        self.project_user = ProjectUser.objects.create(
            user=self.user,
            project=self.project,
            role='developer',
            dept=self.dept_python
        )

        # Initialize clients
        self.client = APIClient()
        self.admin_client = APIClient()
        
        # Authenticate admin user
        admin_refresh = RefreshToken.for_user(self.admin_user)
        admin_access_token = admin_refresh.access_token
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_access_token}')
        
        # Authenticate regular user
        user_refresh = RefreshToken.for_user(self.user)
        user_access_token = user_refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_access_token}')

    def test_project_list_create(self):
        # Test GET request for list of projects
        response = self.client.get(reverse('project-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Test POST request to create a new project
        data = {
            'project_name': 'Project Y',
            'project_duration': 45,
            'client_name': 'Client B',
            'submission_date': '2024-09-01'
        }
        response = self.admin_client.post(reverse('project-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_project_detail(self):
        # Test GET request for a project detail
        response = self.client.get(reverse('project-detail', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], 'Project X')

    def test_project_update(self):
        # Test PUT request to update a project
        data = {
            'project_name': 'Updated Project X',
            'project_duration': 35,
            'client_name': 'Updated Client A',
            'submission_date': '2024-08-15'
        }
        response = self.admin_client.put(reverse('project-detail', kwargs={'pk': self.project.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.get(pk=self.project.pk).project_name, 'Updated Project X')

    def test_project_delete(self):
        # Test DELETE request to remove a project
        response = self.admin_client.delete(reverse('project-detail', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_create_project_user_assignment(self):
        # Test POST request to create a project-user assignment
        data = {
            'user': self.user.pk,
            'project': self.project.pk,
            'role': 'manager',
            'dept': self.dept_python.pk
        }
        response = self.admin_client.post(reverse('project-user-assign'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectUser.objects.count(), 2)

    def test_update_project_status(self):
        # Test PATCH request to update project status
        data = {'status': 'in_progress'}
        response = self.client.patch(reverse('update-project-status', kwargs={'pk': self.project.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.get(pk=self.project.pk).status, 'in_progress')

    def tearDown(self):
        self.user.delete()
        self.admin_user.delete()
        self.project.delete()
        self.dept_python.delete()
        self.project_user.delete()
