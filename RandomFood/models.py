from django.db import models


class FoodCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Food Category"
        verbose_name_plural = "Food Categories"

    def __str__(self):
        return self.name


class FoodType(models.Model):
    """
    Example FoodType entries: 'Thai', 'Noodle', 'Japanese', 'Dessert', 'Soup'
    Food can have many types (e.g., 'Thai' and 'Noodle').
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Food Type"
        verbose_name_plural = "Food Types"

    def __str__(self):
        return self.name


class Food(models.Model):
    foodID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    imageURL = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    favorite_count = models.PositiveIntegerField(default=0)

    # New nutritional fields (in grams)
    protein_in_food = models.FloatField(blank=True, null=True, help_text="Protein (g)")
    carb_in_food = models.FloatField(blank=True, null=True, help_text="Carbohydrates (g)")
    fat_in_food = models.FloatField(blank=True, null=True, help_text="Fat (g)")

    # Ingredients list and category
    ingredients = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated or newline list of ingredients",
    )
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="foods"
    )

    # New: many-to-many types (e.g., Thai, Noodle)
    food_types = models.ManyToManyField(
        FoodType,
        blank=True,
        related_name="foods",
        help_text="Select one or more types for this food (e.g., Thai, Noodle)"
    )

    def __str__(self):
        return self.name
