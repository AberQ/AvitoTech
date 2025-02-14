from rest_framework import serializers
from registration.models import CustomUser
class TransferCoinsSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    amount = serializers.IntegerField(min_value=1)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество монет должно быть положительным числом.")
        return value

    def validate_recipient_email(self, value):
        try:
            recipient = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value