from django.db import models

# Create your models here.
class Merch(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"
    
    
class UserMerch(models.Model):
    user = models.ForeignKey("registration.CustomUser", on_delete=models.CASCADE, related_name="owned_merch")
    merch = models.ForeignKey("Merch", on_delete=models.CASCADE, related_name="owners")
    quantity = models.PositiveIntegerField(default=1)  # Количество одинаковых предметов
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "merch")  # Запрещает дублирующиеся записи (один и тот же товар у одного пользователя)

    def __str__(self):
        return f"{self.user.email} owns {self.quantity}x {self.merch.name}"