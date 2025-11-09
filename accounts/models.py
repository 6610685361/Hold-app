from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Custom Admin สำหรับ User
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
