from django.test import TestCase
from django.contrib import admin
from RandomFood.models import Food, FoodCategory, FoodType


class RandomFoodAdminTest(TestCase):
    def test_admin_registration(self):

        # Check if models are registered
        self.assertIn(Food, admin.site._registry)
        self.assertIn(FoodCategory, admin.site._registry)
        self.assertIn(FoodType, admin.site._registry)
