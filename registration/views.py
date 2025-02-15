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
          
            username = request.data.get("username")
            password = request.data.get("password")

          
            user = User.objects.filter(username=username).first()

            if user:
               
                if not user.check_password(password):
                    return Response(
                        {"description": "Неавторизован."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
              
                serializer = self.get_serializer(data=request.data)

               
                if serializer.is_valid():
                    user = serializer.save()  
                else:
                    return Response(
                        {"description": "Неверный запрос."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

    
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
                {"description": f"Внутренняя ошибка сервера."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
