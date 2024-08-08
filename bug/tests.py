from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Bug
from project.models import Project, ProjectUser
from department.models import Department

User = get_user_model()

class BugTests(TestCase):
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

        # Create bugs
        self.bug = Bug.objects.create(
            bug_type='error',
            created_by=self.user,
            project=self.project,
            department=self.dept_python,
            bug_priority='high',
            bug_severity='major',
            status='open'
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

    def test_bug_list(self):
        # Test GET request for list of bugs
        response = self.client.get(reverse('bug-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_bug_create(self):
        # Test POST request to create a new bug
        data = {
            'bug_type': 'mistake',
            'bug_description': 'Description of a new bug',
            'url_bug': 'http://example.com/bug',
            'bug_priority': 'medium',
            'bug_severity': 'normal',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.post(reverse('bug-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bug.objects.count(), 2)

    def test_bug_detail(self):
        # Test GET request for bug detail
        response = self.client.get(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bug_type'], 'error')

    def test_bug_update(self):
        # Test PUT request to update a bug
        data = {
            'bug_type': 'issue',
            'bug_description': 'Updated description',
            'url_bug': 'http://example.com/updated_bug',
            'bug_priority': 'low',
            'bug_severity': 'minor',
            'status': 'in_progress',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.put(reverse('bug-detail', kwargs={'pk': self.bug.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bug.objects.get(pk=self.bug.pk).bug_type, 'issue')

    def test_bug_delete(self):
        # Test DELETE request to remove a bug
        response = self.client.delete(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bug.objects.count(), 0)

    def test_bug_status_update(self):
        # Test PATCH request to update bug status
        data = {'status': 'closed'}
        response = self.client.patch(reverse('bug-status-update', kwargs={'pk': self.bug.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bug.objects.get(pk=self.bug.pk).status, 'closed')

    def test_bug_create_without_authentication(self):
        # Test that creating a bug without authentication fails
        self.client.credentials()  # Remove authentication
        data = {
            'bug_type': 'error',
            'bug_description': 'Description without authentication',
            'bug_priority': 'high',
            'bug_severity': 'critical',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.post(reverse('bug-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bug_list_admin_access(self):
        # Test that an admin user can see all bugs
        admin_response = self.admin_client.get(reverse('bug-list-create'))
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(admin_response.data), 1)

    def test_bug_detail_admin_access(self):
        # Test that an admin user can access bug details
        admin_response = self.admin_client.get(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin_response.data['bug_type'], 'error')

    def test_bug_update_admin_access(self):
        # Test that an admin user can update a bug
        data = {
            'status': 'closed'
        }
        admin_response = self.admin_client.patch(reverse('bug-status-update', kwargs={'pk': self.bug.pk}), data, format='json')
        self.assertEqual(admin_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Bug.objects.get(pk=self.bug.pk).status, 'closed')

    def test_bug_status_update_by_non_owner(self):
        # Test that a non-owner cannot update the status of a bug
        another_user = User.objects.create_user(username='another_user', password='password')
        another_user_refresh = RefreshToken.for_user(another_user)
        another_user_access_token = another_user_refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {another_user_access_token}')
        data = {'status': 'in_progress'}
        response = self.client.patch(reverse('bug-status-update', kwargs={'pk': self.bug.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bug_list_by_non_owner(self):
        # Test that a non-owner cannot see bugs created by others
        another_user = User.objects.create_user(username='another_user', password='password')
        another_user_refresh = RefreshToken.for_user(another_user)
        another_user_access_token = another_user_refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {another_user_access_token}')
        response = self.client.get(reverse('bug-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_bug_create_with_invalid_data(self):
        # Test that creating a bug with invalid data fails
        data = {
            'bug_type': 'invalid_type',  # Invalid type
            'bug_description': 'Invalid data test',
            'bug_priority': 'medium',
            'bug_severity': 'normal',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.post(reverse('bug-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bug_update_with_invalid_data(self):
        # Test that updating a bug with invalid data fails
        data = {
            'bug_type': 'invalid_type',  # Invalid type
            'bug_description': 'Updated description with invalid type',
            'bug_priority': 'medium',
            'bug_severity': 'normal',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.put(reverse('bug-detail', kwargs={'pk': self.bug.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bug_update_with_missing_fields(self):
        # Test that updating a bug with missing fields fails
        data = {
            'bug_type': 'error',
            # Missing 'bug_description'
            'bug_priority': 'high',
            'bug_severity': 'major',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.put(reverse('bug-detail', kwargs={'pk': self.bug.pk}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bug_list_with_unauthorized_user(self):
        # Test that an unauthorized user cannot access the bug list
        unauthorized_client = APIClient()
        response = unauthorized_client.get(reverse('bug-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bug_detail_with_unauthorized_user(self):
        # Test that an unauthorized user cannot access bug details
        unauthorized_client = APIClient()
        response = unauthorized_client.get(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bug_delete_with_unauthorized_user(self):
        # Test that an unauthorized user cannot delete a bug
        unauthorized_client = APIClient()
        response = unauthorized_client.delete(reverse('bug-detail', kwargs={'pk': self.bug.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bug_status_update_with_unauthorized_user(self):
        # Test that an unauthorized user cannot update bug status
        unauthorized_client = APIClient()
        response = unauthorized_client.patch(reverse('bug-status-update', kwargs={'pk': self.bug.pk}), {'status': 'closed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bug_create_with_missing_auth(self):
        # Test creating a bug with missing authentication
        self.client.credentials()  # Remove authentication
        data = {
            'bug_type': 'error',
            'bug_description': 'No auth',
            'bug_priority': 'low',
            'bug_severity': 'trivial',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.post(reverse('bug-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bug_detail_invalid_id(self):
        # Test GET request with an invalid bug ID
        response = self.client.get(reverse('bug-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bug_update_invalid_id(self):
        # Test PUT request with an invalid bug ID
        data = {
            'bug_type': 'error',
            'bug_description': 'Updated',
            'bug_priority': 'high',
            'bug_severity': 'major',
            'status': 'open',
            'project': self.project.pk,
            'department': self.dept_python.pk
        }
        response = self.client.put(reverse('bug-detail', kwargs={'pk': 9999}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
