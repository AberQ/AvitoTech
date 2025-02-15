from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'date_joined', 'coins')  
    search_fields = ('username',) 
    list_filter = ('is_active', 'is_staff') 
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('coins',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )  

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'coins', 'is_active', 'is_staff')
        }),
    )  

    def save_model(self, request, obj, form, change):
    
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
