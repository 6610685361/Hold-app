from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.profile_url = reverse("profile")
        self.edit_profile_url = reverse("edit_profile")
        self.home_url = reverse("home")

        # สร้าง user สำหรับ test ที่ต้อง login
        self.user = User.objects.create_user(username="tester", password="test12345")

    # ------------------------
    # Register view
    # ------------------------
    def test_register_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_success(self):
        data = {
            "username": "newuser",
            "password1": "NewPass123",
            "password2": "NewPass123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_invalid(self):
        # password ไม่ตรงกัน
        data = {"username": "baduser", "password1": "123", "password2": "456"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertFalse(User.objects.filter(username="baduser").exists())

    # ------------------------
    # Login view
    # ------------------------
    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_success(self):
        data = {"username": "tester", "password": "test12345"}
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.home_url)

    def test_login_fail(self):
        data = {"username": "tester", "password": "wrongpass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")

    # ------------------------
    # Logout view
    # ------------------------
    def test_logout_redirects_to_home(self):
        self.client.login(username="tester", password="test12345")
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)

    # ------------------------
    # Profile view
    # ------------------------
    def test_profile_requires_login(self):
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f"/accounts/login/?next={self.profile_url}")

    def test_profile_page_loads_when_logged_in(self):
        self.client.login(username="tester", password="test12345")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    # ------------------------
    # Edit profile view
    # ------------------------
    def test_edit_profile_get(self):
        self.client.login(username="tester", password="test12345")
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/edit_profile.html")

    def test_edit_profile_post(self):
        self.client.login(username="tester", password="test12345")
        response = self.client.post(self.edit_profile_url, {"username": "tester_new"})
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "tester_new")
        self.assertRedirects(response, self.profile_url)
