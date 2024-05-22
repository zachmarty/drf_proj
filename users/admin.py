from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображения пользователей в админке"""

    list_display = ("id", "email")
