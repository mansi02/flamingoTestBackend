from django.contrib import admin
from custom_user.models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        "first_name",
        "last_name",
        "email",
        "username",
        "profile_image",
        "is_active",
    ]


admin.site.register(User, UserAdmin)
