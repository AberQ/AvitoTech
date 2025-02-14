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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            # Проверяем, существует ли уже пользователь с таким email
            email = request.data.get("email")
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Создаем JWT токены
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "access": access,
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
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
