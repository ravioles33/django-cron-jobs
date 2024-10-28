from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from tutor_profile.models import UserProfile

class UserProfileTests(APITestCase):
    def setUp(self):
        # Crear un usuario para usarlo en las pruebas
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_create_userprofile(self):
        # Prueba para crear un perfil de usuario
        url = reverse('userprofile-list')  # Cambia 'userprofile-list' según el nombre que tenga tu endpoint
        data = {'user': self.user.id, 'lw_username': 'test_lw', 'lw_password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
