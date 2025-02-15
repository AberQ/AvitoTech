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
                # Запись в историю транзакций (по email)
                Transaction.objects.create(
                    user=sender,
                    amount=amount,
                    sender_email=sender.email,
                    recipient_email=recipient.email
                )
            except Exception:
                return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"description": "Успешный ответ!"}, status=status.HTTP_200_OK)

        return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseMerchAPIView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, merch_name):
        try:
            serializer = PurchaseMerchSerializer(data=request.data, context={"request": request, "merch_name": merch_name})
            if serializer.is_valid():
                user_merch = serializer.save()
                
                # Убираем создание транзакции для покупки товара

                return Response(
                    {"description": "Успешный ответ."},
                    status=status.HTTP_200_OK,
                )
            return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)