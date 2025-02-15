from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password   
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainSerializer
from django.db import transaction
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)

            user_data = User.objects.filter(username=username).values("id", "username", "password", "coins").first()

            if user_data:
                if not check_password(password, user_data["password"]):
                    return Response({"description": "Неавторизован."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                hashed_password = make_password(password)
                with transaction.atomic():
                    user = User.objects.create(username=username, password=hashed_password)
                    user_data = {"id": user.id, "username": user.username, "coins": user.coins}

            refresh = RefreshToken.for_user(User(id=user_data["id"]))  # Создаем токен без загрузки объекта из БД
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        
        except Exception as e:
            return Response({"description": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


