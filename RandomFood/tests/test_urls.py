from django.test import TestCase
from django.urls import resolve
from RandomFood.views import add_favorite


class RandomFoodURLsTest(TestCase):
    def test_urls_resolve(self):
        self.assertEqual(resolve("/").func.__name__, "random_food_page")
        self.assertEqual(
            resolve("/api/foods/batch/").func.__name__, "api_random_food_batch"
        )
        self.assertEqual(
            resolve("/api/favorites/add/").func.__name__, "api_add_favorite"
        )
        self.assertEqual(resolve("/api/favorites/").func.__name__, "api_get_favorites")
        self.assertEqual(
            resolve("/remove-favorite/1/").func.__name__, "remove_favorite"
        )
