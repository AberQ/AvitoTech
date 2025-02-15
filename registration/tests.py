from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "http://127.0.0.1:8080/api/auth"  
        self.user_data = {
            "username": "testuser",
            "password": "securepassword"
        }
        self.existing_user = User.objects.create(
            username=self.user_data["username"],
            password=make_password(self.user_data["password"]),
            coins=100
        )
    
    def test_register_new_user(self):
        new_user_data = {"username": "newuser", "password": "newpassword"}
        response = self.client.post(self.url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_login_existing_user(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    def test_invalid_credentials(self):
        invalid_data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["description"], "Неавторизован.")
    
    def test_missing_fields(self):
        response = self.client.post(self.url, {"username": "onlyusername"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["description"], "Неверный запрос.")
    
