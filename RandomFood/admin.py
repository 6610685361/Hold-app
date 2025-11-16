from django.contrib import admin
from .models import Food, FoodCategory, FoodType


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(FoodType)
class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    def food_types_list(self, obj):
        # nice short representation for list_display
        return ", ".join([t.name for t in obj.food_types.all()])

    food_types_list.short_description = "Types"

    list_display = (
        "name",
        "foodID",
        "category",
        "food_types_list",
        "protein_in_food",
        "carb_in_food",
        "fat_in_food",
        "favorite_count",
    )
    list_filter = ("category", "food_types")
    search_fields = ("name", "ingredients", "description")
    readonly_fields = ("foodID",)
    list_editable = ("protein_in_food", "carb_in_food", "fat_in_food")

    # allow easy selection of many-to-many in the form
    filter_horizontal = ("food_types",)

    fieldsets = (
        (None, {"fields": ("foodID", "name", "category", "imageURL")}),
        (
            "Types",
            {
                "fields": ("food_types",),
                "description": "Assign one or more food types (e.g., Thai, Noodle)",
            },
        ),
        (
            "Nutrition (grams)",
            {
                "fields": ("protein_in_food", "carb_in_food", "fat_in_food"),
                "description": "Enter macronutrients in grams",
            },
        ),
        ("Details", {"fields": ("ingredients", "description")}),
    )
