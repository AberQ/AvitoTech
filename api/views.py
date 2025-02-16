from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import *
from registration.models import CustomUser

from .serializers import *


class TransferCoinsView(generics.GenericAPIView):
    serializer_class = TransferCoinsSerializer
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            sender = request.user  
            recipient_username = serializer.validated_data['toUser']  
            amount = serializer.validated_data['amount']
            if sender.username == recipient_username:
                return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)
            if sender.coins < amount:
                return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                recipient = CustomUser.objects.get(username=recipient_username)  
            except CustomUser.DoesNotExist:
                return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            sender.coins -= amount
            recipient.coins += amount

            try:
                sender.save()
                recipient.save()
                
                Transaction.objects.create(
                    user=sender,
                    amount=amount,
                    sender_username=sender.username,  
                    recipient_username=recipient.username  
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
                
                return Response(
                    {"description": "Успешный ответ."},
                    status=status.HTTP_200_OK,
                )
            return Response({"description": "Неверный запрос."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"description": "Внутренняя ошибка сервера."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserInfoAPIView(APIView): 
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        try:
            user = request.user
            serializer = UserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({"error": "Неавторизован"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": f"Внутренняя ошибка сервера: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)