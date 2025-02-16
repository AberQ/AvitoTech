from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Transaction

User = get_user_model()

class UserInfoAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", coins=100)
        self.other_user = User.objects.create_user(username="otheruser", password="testpassword", coins=50)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("user-info")  # Укажи правильное имя URL

        # Создаем тестовые транзакции
        Transaction.objects.create(user=self.user, amount=10, sender_username=self.user.username, recipient_username=self.other_user.username)
        Transaction.objects.create(user=self.other_user, amount=5, sender_username=self.other_user.username, recipient_username=self.user.username)

    def test_authentication_required(self):
        """Тестирует, что без авторизации доступ запрещен"""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_response(self):
        """Тестирует корректность данных, возвращаемых API"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "username": self.user.username,
            "coins": self.user.coins,
            "inventory": [],
            "coin_history": {
                "sent": [{"toUser": "otheruser", "amount": 10}],
                "received": [{"fromUser": "otheruser", "amount": 5}]
            }
        }
        self.assertEqual(response.json(), expected_data)

    @patch("api.serializers.UserMerchSerializer.data", return_value=[])
    def test_inventory_mock(self, mock_inventory):
        """Тестируем, что inventory возвращает пустой список (mock UserMerchSerializer)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["inventory"], [])
