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