from rest_framework import serializers
from registration.models import CustomUser
from .models import *
class TransferCoinsSerializer(serializers.Serializer):
    toUser = serializers.EmailField()  # Переименовываем поле в toUser
    amount = serializers.IntegerField(min_value=1)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество монет должно быть положительным числом.")
        return value

    def validate_toUser(self, value):
        try:
            recipient = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    
class PurchaseMerchSerializer(serializers.Serializer):
    def validate(self, attrs):
        merch_name = self.context["merch_name"]  # Извлекаем merch_name из контекста
        user = self.context["request"].user
        try:
            merch = Merch.objects.get(name=merch_name)
        except Merch.DoesNotExist:
            raise serializers.ValidationError("Товар с таким названием не найден.")

        # Проверяем, достаточно ли монет у пользователя
        total_price = merch.price
        if user.coins < total_price:
            raise serializers.ValidationError("Недостаточно монет для покупки.")

        return attrs

    def save(self):
        user = self.context["request"].user
        merch_name = self.context["merch_name"]
        merch = Merch.objects.get(name=merch_name)
        total_price = merch.price

        # Снимаем монеты с баланса пользователя
        user.coins -= total_price
        user.save()

        # Добавляем или обновляем запись о товаре у пользователя
        user_merch, created = UserMerch.objects.get_or_create(user=user, merch=merch)
        if not created:
            user_merch.quantity += 1
            user_merch.save()

        return user_merch
    
    
    
class UserMerchSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='merch.name')  # Меняем 'merch_name' на 'type'

    class Meta:
        model = UserMerch
        fields = ['type', 'quantity']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("amount", "sender_email", "recipient_email", "timestamp")


class UserInfoSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()
    coin_history = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("email", "coins", "inventory", "coin_history")

    def get_inventory(self, obj):
        user_merch = obj.owned_merch.all()
        return {
            "items": UserMerchSerializer(user_merch, many=True).data
        }

    def get_coin_history(self, obj):
        # Получаем все транзакции, где пользователь является отправителем или получателем
        sent_transactions = Transaction.objects.filter(sender_email=obj.email)
        received_transactions = Transaction.objects.filter(recipient_email=obj.email)
        
        # Формируем список отправленных транзакций
        sent = [
            {
                "toUser": transaction.recipient_email,
                "amount": transaction.amount
            }
            for transaction in sent_transactions
        ]
        
        # Формируем список полученных транзакций
        received = [
            {
                "fromUser": transaction.sender_email,
                "amount": transaction.amount
            }
            for transaction in received_transactions
        ]
        
        return {
            "received": received,
            "sent": sent
        }
