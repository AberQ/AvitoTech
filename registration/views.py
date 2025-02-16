from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import update_last_login
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken




User = get_user_model()

class RegisterView(generics.CreateAPIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(username=username).first()

            if user:
                if not check_password(password, user.password):
                    return Response({"description": "Неавторизован."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                hashed_password = make_password(password)
                with transaction.atomic():
                    user = User.objects.create(username=username, password=hashed_password)

            
            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response({"description": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
