from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "bio",
                    "role", "confirmation_code", 'is_staff')


admin.site.register(User, UserAdmin)