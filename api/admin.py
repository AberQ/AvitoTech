from django.contrib import admin
from .models import Merch, UserMerch, Transaction


class MerchAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 
    search_fields = ('name',) 
    ordering = ('name',)  
    list_filter = ('price',) 

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class UserMerchAdmin(admin.ModelAdmin):
    list_display = ('user', 'merch', 'quantity', 'acquired_at')  
    search_fields = ('user__username', 'merch__name')  
    list_filter = ('acquired_at',)  
    raw_id_fields = ('user', 'merch')  

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'sender_username', 'recipient_username', 'timestamp')  
    search_fields = ('user__username', 'sender_username', 'recipient_username')  
    list_filter = ('timestamp',) 
    ordering = ('-timestamp',)  

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)



admin.site.register(Merch, MerchAdmin)
admin.site.register(UserMerch, UserMerchAdmin)
admin.site.register(Transaction, TransactionAdmin)
