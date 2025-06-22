from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Кастомная административная панель для модели User. Наследует стандартный UserAdmin и добавляет/изменяет:
        - Поддержку дополнительных полей (телефон, город, аватар, Telegram ID)
        - Удаление поля username из всех форм
        - Кастомное отображение списка пользователей
    get_form: Удаляет поле username из формы пользователя"""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'city', 'avatar', 'tg_chat_id')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Удаляем все упоминания username
    def get_form(self, request, obj=None, **kwargs):
        """Удаляет поле username из формы пользователя.
        Переопределяет стандартное поведение UserAdmin для полного исключения username из интерфейса администратора"""

        form = super().get_form(request, obj, **kwargs)
        if 'username' in form.base_fields:
            del form.base_fields['username']
        return form
