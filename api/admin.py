from django.contrib import admin
from .models import Merch, UserMerch, Transaction

# Регистрация модели Merch
class MerchAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Отображаемые поля
    search_fields = ('name',)  # Возможность поиска по имени товара

# Регистрация модели UserMerch
class UserMerchAdmin(admin.ModelAdmin):
    list_display = ('user', 'merch', 'quantity', 'acquired_at')  # Отображаемые поля
    list_filter = ('user', 'merch')  # Фильтры для отображения
    search_fields = ('user__email', 'merch__name')  # Поиск по email пользователя и названию товара

# Регистрация модели Transaction
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'sender_email', 'recipient_email', 'timestamp')  # Отображаемые поля
    list_filter = ('user', 'timestamp')  # Фильтры по пользователю и времени
    search_fields = ('sender_email', 'recipient_email')  # Поиск по email

# Регистрируем модели и их кастомные админки
admin.site.register(Merch, MerchAdmin)
admin.site.register(UserMerch, UserMerchAdmin)
admin.site.register(Transaction, TransactionAdmin)
