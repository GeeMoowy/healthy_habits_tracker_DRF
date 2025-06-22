from django.contrib import admin
from habits.models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления привычками.
    Настройки отображения и функциональности модели Habit в Django Admin."""

    list_display = ('id', 'user', 'action', 'time', 'place', 'periodicity_display', 'is_pleasant')
    list_filter = ('is_pleasant', 'is_public', 'user')
    search_fields = ('action', 'place', 'user__email')
    readonly_fields = ('periodicity_display',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Настройки привычки', {
            'fields': ('is_pleasant', 'related_habit', 'reward', 'periodicity_days', 'time_to_complete')
        }),
        ('Видимость', {
            'fields': ('is_public',)
        }),
    )

    def periodicity_display(self, obj):
        """Отображает удобочитаемое представление периодичности привычки."""

        return obj.periodicity_display
    periodicity_display.short_description = 'Периодичность'