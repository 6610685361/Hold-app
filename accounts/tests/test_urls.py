from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import register, profile, edit_profile, user_logout
from django.contrib.auth.views import LoginView


class AccountsURLsTests(SimpleTestCase):

    # register/
    def test_register_url_resolves(self):
        url = reverse("register")
        self.assertEqual(resolve(url).func, register)

    # login/
    def test_login_url_resolves(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginView)

    # logout/
    def test_logout_url_resolves(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, user_logout)

    # profile/
    def test_profile_url_resolves(self):
        url = reverse("profile")
        self.assertEqual(resolve(url).func, profile)

    # edit_profile/
    def test_edit_profile_url_resolves(self):
        url = reverse("edit_profile")
        self.assertEqual(resolve(url).func, edit_profile)
