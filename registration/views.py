from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            # Извлекаем данные из запроса
            username = request.data.get("username")
            password = request.data.get("password")

            # Проверяем, существует ли пользователь с таким username
            user = User.objects.filter(username=username).first()

            if user:
                # Если пользователь существует, проверяем пароль
                if not user.check_password(password):
                    return Response(
                        {"description": "Неверный пароль."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                # Если пользователя нет, проверяем данные через сериализатор
                serializer = self.get_serializer(data=request.data)

                # Проверяем, что данные валидны
                if serializer.is_valid():
                    user = serializer.save()  # Сохраняем нового пользователя
                else:
                    return Response(
                        {"description": "Некорректные данные."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Создаем JWT токены
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                    },
                    "access": access,
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK if user else status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"description": f"Внутренняя ошибка сервера: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавь `rest_framework_simplejwt.token_blacklist` в `INSTALLED_APPS`
            return Response({"message": "Вы вышли из системы"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
