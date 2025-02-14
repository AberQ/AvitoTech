from django.db import models

# Create your models here.
class Merch(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.price}"