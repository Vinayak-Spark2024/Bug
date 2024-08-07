from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from department.models import Department
from .models import Project

User = get_user_model()

class ProjectTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='userpassword',
            email='user@example.com'
        )
        # Create a department for both users
        self.department_admin = Department.objects.create(
            user=self.admin_user,
            department='Development',
            role='Developer'
        )
        self.department_user = Department.objects.create(
            user=self.regular_user,
            department='Management',
            role='Manager'
        )
        # URL for the API endpoints
        self.list_create_url = reverse('project-list')
        self.detail_url = lambda pk: reverse('project-detail', kwargs={'pk': pk})

    def authenticate_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_for_user(self.admin_user))

    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_for_user(self.regular_user))

    def get_jwt_for_user(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_project_as_admin(self):
        self.authenticate_admin()
        data = {
            "project_name": "Project Alpha",
            "project_description": "Description of Project Alpha.",
            "project_duration": 100,
            "client_name": "Client ABC",
            "submission_date": "2024-12-31"
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().project_name, "Project Alpha")

    def test_create_project_as_regular_user(self):
        self.authenticate_user()
        data = {
            "project_name": "Project Beta",
            "project_description": "Description of Project Beta.",
            "project_duration": 200,
            "client_name": "Client XYZ",
            "submission_date": "2024-11-30"
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 0)

    def test_list_projects_as_admin(self):
        self.authenticate_admin()
        Project.objects.create(
            project_name="Project Gamma",
            project_description="Description of Project Gamma.",
            project_duration=150,
            client_name="Client DEF",
            submission_date="2025-01-15",
            user=self.admin_user,
            department=self.department_admin
        )
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_projects_as_regular_user(self):
        self.authenticate_user()
        Project.objects.create(
            project_name="Project Delta",
            project_description="Description of Project Delta.",
            project_duration=180,
            client_name="Client GHI",
            submission_date="2024-11-30",
            user=self.admin_user,
            department=self.department_admin
        )
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_project_as_admin(self):
        self.authenticate_admin()
        project = Project.objects.create(
            project_name="Project Epsilon",
            project_description="Description of Project Epsilon.",
            project_duration=75,
            client_name="Client JKL",
            submission_date="2024-09-15",
            user=self.admin_user,
            department=self.department_admin
        )
        response = self.client.get(self.detail_url(project.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], "Project Epsilon")

    def test_retrieve_project_as_regular_user(self):
        self.authenticate_user()
        project = Project.objects.create(
            project_name="Project Zeta",
            project_description="Description of Project Zeta.",
            project_duration=90,
            client_name="Client MNO",
            submission_date="2024-10-20",
            user=self.admin_user,
            department=self.department_admin
        )
        response = self.client.get(self.detail_url(project.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)  # Ensure the 'detail' key is in the response
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')  # Check the error message



    def test_update_project_as_admin(self):
        self.authenticate_admin()
        project = Project.objects.create(
            project_name="Project Eta",
            project_description="Description of Project Eta.",
            project_duration=120,
            client_name="Client PQR",
            submission_date="2024-08-30",
            user=self.admin_user,
            department=self.department_admin
        )
        data = {
            "project_name": "Project Eta Updated",
            "project_description": "Updated description.",
            "project_duration": 150,
            "client_name": "Client PQR Updated",
            "submission_date": "2024-09-30"
        }
        response = self.client.put(self.detail_url(project.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.project_name, "Project Eta Updated")

    def test_update_project_as_regular_user(self):
        self.authenticate_user()
        project = Project.objects.create(
            project_name="Project Theta",
            project_description="Description of Project Theta.",
            project_duration=130,
            client_name="Client STU",
            submission_date="2024-07-15",
            user=self.admin_user,
            department=self.department_admin
        )
        data = {
            "project_name": "Project Theta Updated",
            "project_description": "Updated description.",
            "project_duration": 160,
            "client_name": "Client STU Updated",
            "submission_date": "2024-08-15"
        }
        response = self.client.put(self.detail_url(project.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_project_as_admin(self):
        self.authenticate_admin()
        project = Project.objects.create(
            project_name="Project Iota",
            project_description="Description of Project Iota.",
            project_duration=140,
            client_name="Client VWX",
            submission_date="2024-06-30",
            user=self.admin_user,
            department=self.department_admin
        )
        response = self.client.delete(self.detail_url(project.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_delete_project_as_regular_user(self):
        self.authenticate_user()
        project = Project.objects.create(
            project_name="Project Kappa",
            project_description="Description of Project Kappa.",
            project_duration=110,
            client_name="Client YZA",
            submission_date="2024-05-30",
            user=self.admin_user,
            department=self.department_admin
        )
        response = self.client.delete(self.detail_url(project.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)  # Ensure the project was not deleted

    def test_unauthorized_access(self):
        # Test that unauthorized users cannot access or modify projects
        data = {
            "project_name": "Unauthorized Project",
            "project_description": "This project should not be created.",
            "project_duration": 50,
            "client_name": "Unauthorized Client",
            "submission_date": "2024-08-30"
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
