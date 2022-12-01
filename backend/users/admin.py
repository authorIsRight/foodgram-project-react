from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Поля видимости в админке"""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )

    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)