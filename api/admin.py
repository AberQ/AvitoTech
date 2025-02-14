from django.contrib import admin
from .models import *

@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_filter = ("price",)
@admin.register(UserMerch)
class UserMerchAdmin(admin.ModelAdmin):
    list_display = ("user", "merch", "quantity", "acquired_at")
    list_filter = ("acquired_at",)
    search_fields = ("user__email", "merch__name")
    
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_type", "amount", "sender_email", "recipient_email", "merch_name", "timestamp")
    list_filter = ("transaction_type", "timestamp")
    search_fields = ("sender_email", "recipient_email", "merch_name")
    ordering = ("-timestamp",)
