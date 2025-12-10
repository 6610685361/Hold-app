from django.test import TestCase
from RandomFood.models import Food, FoodCategory, FoodType


class RandomFoodModelsTest(TestCase):
    def setUp(self):
        self.category = FoodCategory.objects.create(name="Dessert")
        self.type1 = FoodType.objects.create(name="Sweet")
        self.food = Food.objects.create(
            name="Ice Cream",
            category=self.category,
            favorite_count=0,
        )
        self.food.food_types.add(self.type1)

    def test_food_str(self):
        self.assertEqual(str(self.food), "Ice Cream")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Dessert")

    def test_food_type_str(self):
        self.assertEqual(str(self.type1), "Sweet")

    def test_food_food_types_relation(self):
        self.assertIn(self.type1, self.food.food_types.all())
