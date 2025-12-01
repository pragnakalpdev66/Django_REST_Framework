from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ExceptionHandlerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_authentication_error(self):
        # Request without token
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error']['details']['code'], 'authentication_required')

    def test_validation_error(self):
        # Login
        self.client.force_authenticate(user=self.user)

        # Invalid data - empty title
        response = self.client.post('/api/tasks/', {
            'title': '',
            'completed': False
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn('fields', response.data['error']['details'])
        self.assertIn('title', response.data['error']['details']['fields'])

    def test_permission_denied(self):
        # Login as regular user
        self.client.force_authenticate(user=self.user)

        # Try to access admin-only endpoint (if you have one)
        # This would return 403 if permission denied
        # response = self.client.get('/api/admin/tasks/')
        # self.assertEqual(response.status_code, 403)