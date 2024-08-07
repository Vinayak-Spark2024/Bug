from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from department.models import Department
from accounts.models import CustomUser
from datetime import date, timedelta


class ProjectSerializerTestCase(TestCase):
    def setUp(self):
        # Create a CustomUser instance
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a Department instance
        self.department = Department.objects.create(
            user=self.user,
            department='DevOps',
            role='Developer'
        )

        # Create a Project instance
        self.project = Project.objects.create(
            project_name='Test Project',
            project_description='Description of test project',
            project_duration=30,
            client_name='Test Client',
            department=self.department,
            submission_date=date.today()
        )

    def test_project_serializer(self):
        serializer = ProjectSerializer(instance=self.project)
        data = serializer.data

        self.assertEqual(data['project_name'], self.project.project_name)
        self.assertEqual(data['project_description'], self.project.project_description)
        self.assertEqual(data['project_duration'], self.project.project_duration)
        self.assertEqual(data['client_name'], self.project.client_name)
        self.assertEqual(data['department'], self.department.id)  # Check foreign key reference
        self.assertEqual(data['submission_date'], self.project.submission_date.isoformat())
        self.assertEqual(data['updated_date'], self.project.updated_date.isoformat())  # auto_now=True field

    def test_project_creation(self):
        data = {
            'project_name': 'New Project',
            'project_description': 'Description of new project',
            'project_duration': 45,
            'client_name': 'New Client',
            'department': self.department.id,
            'submission_date': '2024-08-01'
        }
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.latest('id').project_name, 'New Project')

    def test_project_update(self):
        data = {
            'project_name': 'Updated Project',
            'project_description': 'Updated description',
            'project_duration': 60,
            'client_name': 'Updated Client',
            'department': self.department.id,
            'submission_date': '2024-09-01'
        }
        response = self.client.put(f'/api/projects/{self.project.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.project_name, 'Updated Project')

    def test_project_partial_update(self):
        data = {
            'project_description': 'Partially updated description'
        }
        response = self.client.patch(f'/api/projects/{self.project.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.project_description, 'Partially updated description')

    def test_project_deletion(self):
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_project_retrieval(self):
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], self.project.project_name)

    def test_project_list(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_invalid_project_creation(self):
        data = {
            'project_name': '',
            'project_description': 'Description without a name',
            'project_duration': -10,  # Invalid duration
            'client_name': 'Client without a name',
            'department': self.department.id,
            'submission_date': '2024-08-01'
        }
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_field_in_creation(self):
        data = {
            'project_name': 'Project with missing field',
            'project_description': 'Description with missing field',
            'client_name': 'Client with missing department',
            'submission_date': '2024-08-01'
        }
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_serializer_with_missing_fields(self):
        incomplete_data = {
            'project_name': 'Incomplete Project',
            'client_name': 'Client with missing fields'
            # Missing 'project_description', 'project_duration', 'department', 'submission_date'
        }
        serializer = ProjectSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'project_description', 'project_duration', 'department', 'submission_date'})

    def test_invalid_submission_date(self):
        data = {
            'project_name': 'Project with Invalid Date',
            'project_description': 'Description with invalid date',
            'project_duration': 30,
            'client_name': 'Client with invalid date',
            'department': self.department.id,
            'submission_date': 'invalid-date'
        }
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_existent_project(self):
        data = {
            'project_name': 'Non-existent Project Update',
            'project_description': 'Update to a non-existent project',
            'project_duration': 45,
            'client_name': 'Client',
            'department': self.department.id,
            'submission_date': '2024-08-01'
        }
        response = self.client.put('/api/projects/999/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_non_existent_project(self):
        data = {
            'project_description': 'Partial update to a non-existent project'
        }
        response = self.client.patch('/api/projects/999/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_projects_by_valid_department(self):
        response = self.client.get(f'/api/projects/?department={self.department.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.project.project_name, [proj['project_name'] for proj in response.data])

    def test_list_projects_by_invalid_department(self):
        response = self.client.get('/api/projects/?department=999')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_project_without_authentication(self):
        self.client.logout()
        data = {
            'project_name': 'Unauthorized Update',
            'project_description': 'Update without authentication',
            'project_duration': 50,
            'client_name': 'Client',
            'department': self.department.id,
            'submission_date': '2024-08-01'
        }
        response = self.client.put(f'/api/projects/{self.project.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_project_without_authentication(self):
        self.client.logout()
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_serializer_validations(self):
        invalid_data = {
            'project_name': 'Valid Name',
            'project_description': 'Valid description',
            'project_duration': 10,
            'client_name': 'Valid Client',
            'department': self.department.id,
            'submission_date': '2024-08-01'
            # Missing required fields to test validation
        }
        serializer = ProjectSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('updated_date', serializer.errors)

    def test_default_updated_date(self):
        data = {
            'project_name': 'Default Updated Date',
            'project_description': 'Testing default updated date',
            'project_duration': 30,
            'client_name': 'Client',
            'department': self.department.id,
            'submission_date': '2024-08-01'
        }
        response = self.client.post('/api/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(project_name='Default Updated Date')
        self.assertIsNotNone(project.updated_date)