from django.contrib import admin
from .models import Merch, UserMerch, Transaction


class MerchAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # отображение в списке
    search_fields = ('name',)  # поиск по названию товара
    ordering = ('name',)  # сортировка по имени товара
    list_filter = ('price',)  # фильтрация по цене товара

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class UserMerchAdmin(admin.ModelAdmin):
    list_display = ('user', 'merch', 'quantity', 'acquired_at')  # отображение в списке
    search_fields = ('user__username', 'merch__name')  # поиск по пользователю и товару
    list_filter = ('acquired_at',)  # фильтрация по времени получения товара
    raw_id_fields = ('user', 'merch')  # улучшение производительности, если у пользователя много товаров

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'sender_username', 'recipient_username', 'timestamp')  # отображение в списке
    search_fields = ('user__username', 'sender_username', 'recipient_username')  # поиск по пользователю и отправителям/получателям
    list_filter = ('timestamp',)  # фильтрация по времени транзакции
    ordering = ('-timestamp',)  # сортировка по времени транзакции (по убыванию)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# Регистрация моделей в админке
admin.site.register(Merch, MerchAdmin)
admin.site.register(UserMerch, UserMerchAdmin)
admin.site.register(Transaction, TransactionAdmin)
