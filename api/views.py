from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from registration.models import CustomUser
from .serializers import TransferCoinsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import BasePermission

class IsAuthenticatedCustom(BasePermission):
    """Кастомное разрешение, которое выбрасывает AuthenticationFailed с уникальным описанием"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed("Неавторизован")
        return True

class TransferCoinsView(generics.GenericAPIView):
    serializer_class = TransferCoinsSerializer
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sender = request.user  # Текущий пользователь (отправитель)
            recipient_email = serializer.validated_data['recipient_email']
            amount = serializer.validated_data['amount']

            if sender.coins < amount:
                return Response({"detail": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                recipient = CustomUser.objects.get(email=recipient_email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "Получатель не найден."}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                return Response({"detail": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Перевод монет
            sender.coins -= amount
            recipient.coins += amount

            try:
                sender.save()
                recipient.save()
            except Exception:
                return Response({"detail": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"detail": "Успешный ответ!"}, status=status.HTTP_200_OK)

        # В случае ошибки сериализации всегда возвращаем одинаковое сообщение
        return Response({"detail": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)