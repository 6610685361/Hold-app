from django.contrib import admin
from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "foodID", "favorite_count", "description")
    ordering = ("-favorite_count",)
    search_fields = ("name", "description")
    list_filter = ("favorite_count",)
