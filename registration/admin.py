from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'date_joined', 'coins')  # поля для отображения в списке
    search_fields = ('username',)  # позволяет искать по полю username
    list_filter = ('is_active', 'is_staff')  # фильтрация по этим полям
    ordering = ('-date_joined',)  # сортировка по дате регистрации (по убыванию)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('coins',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )  # разделение полей на блоки для улучшенного отображения

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'coins', 'is_active', 'is_staff')
        }),
    )  # поля для регистрации нового пользователя

    def save_model(self, request, obj, form, change):
        # Дополнительная логика при сохранении объекта (например, отправка email)
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
