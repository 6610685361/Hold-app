from django.test import TestCase, Client
from django.contrib.auth.models import User
from RandomFood.models import Food, FoodCategory
from django.urls import reverse


class MainViewsTest(TestCase):
    """Unit tests for main/views.py"""

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="adminuser", password="12345", is_staff=True
        )
        category = FoodCategory.objects.create(name="Dessert")
        for i in range(15):
            Food.objects.create(name=f"Food{i}", favorite_count=i, category=category)

    def test_home_view(self):
        """Test that the home view returns status 200 and uses the correct template"""
        response = self.client.get(reverse("random_food_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "RandomFood/home.html")

    def test_about_view(self):
        """Test the about page view renders correctly"""
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/AboutUs.html")

    def test_admin_dashboard_requires_staff(self):
        """Test that admin_dashboard redirects non-staff users"""
        user = User.objects.create_user(username="normal", password="12345")
        self.client.login(username="normal", password="12345")
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_admin_dashboard_view(self):
        """Test that staff user can access admin_dashboard and top_foods are correct"""
        self.client.login(username="adminuser", password="12345")
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/admin_dashboard.html")

        top_foods = list(
            response.context["top_foods"]
        )  # Convert QuerySet slice to list
        self.assertEqual(len(top_foods), 10)
        self.assertEqual(top_foods[0].favorite_count, 14)
        self.assertEqual(top_foods[-1].favorite_count, 5)
