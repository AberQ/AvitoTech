from django.contrib import admin
from .models import Merch

@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
    list_filter = ("price",)
