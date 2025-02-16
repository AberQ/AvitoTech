from django.db import models

from registration.models import *


class Merch(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"
    
    
class UserMerch(models.Model):
    user = models.ForeignKey("registration.CustomUser", on_delete=models.CASCADE, related_name="owned_merch", db_index=True)
    merch = models.ForeignKey("Merch", on_delete=models.CASCADE, related_name="owners", db_index=True)
    quantity = models.PositiveIntegerField(default=1) 
    acquired_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "merch") 

    def __str__(self):
        return f"{self.user.username} owns {self.quantity}x {self.merch.name}"
    
    
    
class Transaction(models.Model):


    user = models.ForeignKey("registration.CustomUser", on_delete=models.CASCADE, related_name="transactions")
    amount = models.PositiveIntegerField()
    sender_username = models.CharField(max_length=150, null=True, blank=True, db_index=True) 
    recipient_username = models.CharField(max_length=150, null=True, blank=True, db_index=True)  
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} coins"