from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import home, about


class MainURLsTests(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, home)

    def test_about_url_resolves(self):
        url = reverse("about")
        self.assertEqual(resolve(url).func, about)
