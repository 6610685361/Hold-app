from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import admin
from RandomFood.models import Food, FoodCategory, FoodType
from RandomFood.views import add_favorite
from accounts.models import UserProfile
import json


class RandomFoodViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user)
        self.category = FoodCategory.objects.create(name="Dessert")
        self.type1 = FoodType.objects.create(name="Sweet")
        self.food = Food.objects.create(
            name="Ice Cream",
            category=self.category,
            favorite_count=0,
        )
        self.food.food_types.add(self.type1)

    # ทดสอบหน้า HTML หลัก random_food_page
    def test_random_food_page(self):
        response = self.client.get(reverse("random_food_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RandomFood/home.html")
        self.assertIn("categories", response.context)
        self.assertIn("types", response.context)

    def test_api_random_food_batch_default(self):
        response = self.client.get(reverse("api_random_food_batch"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cards", data)
        self.assertIn("done", data)
        self.assertTrue(len(data["cards"]) >= 1)

    def test_api_random_food_batch_with_params(self):
        response = self.client.get(
            reverse("api_random_food_batch"),
            {"category": self.category.id, "types": str(self.type1.id), "n": 1},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["cards"]), 1)
        self.assertEqual(data["cards"][0]["id"], self.food.pk)

    def test_invalid_n_and_offset(self):
        """Test invalid 'n' and 'offset' to hit first except block"""
        response = self.client.get(
            reverse("api_random_food_batch"), {"n": "abc", "offset": "xyz"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should still return valid JSON with cards
        self.assertIn("cards", data)

    def test_invalid_category(self):
        """Test invalid category triggers category except"""
        response = self.client.get(
            reverse("api_random_food_batch"), {"category": "notanint"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cards", data)

    def test_invalid_types(self):
        """Test invalid types param triggers types except"""
        response = self.client.get(
            reverse("api_random_food_batch"), {"types": "1,abc,3"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cards", data)

    def test_empty_queryset(self):
        """Test case where no food matches filters (hits early return)"""
        # Use a category id that doesn't exist
        response = self.client.get(reverse("api_random_food_batch"), {"category": 999})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {"cards": [], "done": True})

    def test_add_favorite_requires_login(self):
        response = self.client.post(reverse("remove_favorite", args=[self.food.pk]))
        self.assertEqual(response.status_code, 302)  # redirects to login

    def test_api_get_favorites(self):
        self.client.login(username="testuser", password="12345")
        profile = self.profile
        profile.favorites.add(self.food)
        response = self.client.get(reverse("api_get_favorites"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["favorites"]), 1)
        self.assertEqual(data["favorites"][0]["id"], self.food.pk)

    def test_remove_favorite(self):
        self.client.login(username="testuser", password="12345")
        profile = self.profile
        profile.favorites.add(self.food)
        response = self.client.get(reverse("remove_favorite", args=[self.food.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        profile.refresh_from_db()
        self.assertNotIn(self.food, profile.favorites.all())


class AddFavoriteViewTest(TestCase):
    """Unit test to cover add_favorite view"""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user)
        self.category = FoodCategory.objects.create(name="Dessert")
        self.type1 = FoodType.objects.create(name="Sweet")
        self.food = Food.objects.create(name="Ice Cream", category=self.category)
        self.food.food_types.add(self.type1)
        self.url = reverse("api_add_favorite")

    def test_add_favorite_when_not_in_favorites(self):
        """Test adding a food not already in favorites"""
        request = self.factory.get(f"/add_favorite/{self.food.pk}/")
        request.user = self.user

        response = add_favorite(request, self.food.pk)
        data = json.loads(response.content)

        # Inverted logic: food not in favorites => "removed" and decrement
        self.assertEqual(data["ok"], True)
        self.assertEqual(data["action"], "removed")
        self.assertEqual(
            data["favorite_count"], 0
        )  # starts at 0, decremented but min 0

        # Food should be added to favorites anyway
        self.assertIn(self.food, self.profile.favorites.all())

    def test_add_favorite_when_already_in_favorites(self):
        """Test adding a food that is already in favorites"""
        self.profile.favorites.add(self.food)
        self.food.favorite_count = 1
        self.food.save()

        request = self.factory.get(f"/add_favorite/{self.food.pk}/")
        request.user = self.user

        response = add_favorite(request, self.food.pk)
        data = json.loads(response.content)

        # Inverted logic: food in favorites => "added" and increment
        self.assertEqual(data["ok"], True)
        self.assertEqual(data["action"], "added")
        self.assertEqual(data["favorite_count"], 2)  # incremented from 1

    def test_non_post_method(self):
        """Test GET request returns 405"""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Only POST allowed"})

    def test_missing_food_id(self):
        """Test POST with no food_id returns 400"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            self.url, data=json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "No dish_id provided"})

    def test_invalid_food_id(self):
        """Test POST with non-existent food_id triggers except block"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            self.url,
            data=json.dumps({"food_id": 999}),  # invalid id
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_add_favorite_success(self):
        """Test normal POST adding favorite"""
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            self.url,
            data=json.dumps({"food_id": self.food.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "added")
        self.assertIn(self.food, self.profile.favorites.all())

    def test_remove_favorite_success(self):
        """Test POST removing favorite"""
        self.client.login(username="testuser", password="12345")
        self.profile.favorites.add(self.food)
        self.food.favorite_count = 1
        self.food.save()

        response = self.client.post(
            self.url,
            data=json.dumps({"food_id": self.food.pk}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "removed")
        self.profile.refresh_from_db()
        self.assertNotIn(self.food, self.profile.favorites.all())
