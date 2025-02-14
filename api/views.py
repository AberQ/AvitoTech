from rest_framework import status, generics
from rest_framework.response import Response
from registration.models import CustomUser
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from base.utils import *

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
                return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                recipient = CustomUser.objects.get(email=recipient_email)
            except CustomUser.DoesNotExist:
                return Response({"description": "Получатель не найден."}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Перевод монет
            sender.coins -= amount
            recipient.coins += amount

            try:
                sender.save()
                recipient.save()
            except Exception:
                return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"description": "Успешный ответ!"}, status=status.HTTP_200_OK)

        # В случае ошибки сериализации всегда возвращаем одинаковое сообщение
        return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class PurchaseMerchAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, merch_name):
        try:
            # Передаем merch_name в контексте
            serializer = PurchaseMerchSerializer(data=request.data, context={"request": request, "merch_name": merch_name})
            if serializer.is_valid():
                user_merch = serializer.save()
                return Response(
                    {"description": f"Успешный ответ."},
                    status=status.HTTP_200_OK,
                )
            return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # В случае ошибки возвращаем сообщение о внутренней ошибке
            return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)