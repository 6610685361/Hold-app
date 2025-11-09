from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewsTests(TestCase):

    # ✅ 1) ทดสอบว่าเปิดหน้า register ได้
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    # ✅ 2) ทดสอบสมัครสมาชิกสำเร็จ
    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        # สมัครแล้วต้อง redirect ไปหน้า home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        # และผู้ใช้ต้องถูกสร้างจริง
        self.assertTrue(User.objects.filter(username="testuser").exists())

    # ✅ 3) ทดสอบเปิดหน้า login ได้
    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    # ✅ 4) ทดสอบ login สำเร็จ
    def test_login_success(self):
        User.objects.create_user(username="testuser", password="StrongPass123!")

        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "StrongPass123!"}
        )

        self.assertEqual(response.status_code, 302)

    # ✅ 5) ทดสอบหน้า profile ต้อง login ก่อน
    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # redirect to login
        self.assertIn(reverse("login"), response.url)

    # ✅ 6) ทดสอบดูหน้า profile สำเร็จ
    def test_profile_page_loads_when_logged_in(self):
        user = User.objects.create_user(username="testuser", password="StrongPass123!")
        self.client.login(username="testuser", password="StrongPass123!")

        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    # ✅ 7) ทดสอบ edit profile ต้อง login ก่อน
    def test_edit_profile_requires_login(self):
        response = self.client.get(reverse("edit_profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    # ✅ 8) ทดสอบแก้ไข profile สำเร็จ
    def test_edit_profile_success(self):
        user = User.objects.create_user(username="testuser", password="StrongPass123!")
        self.client.login(username="testuser", password="StrongPass123!")

        response = self.client.post(
            reverse("edit_profile"), {"username": "updateduser"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile"))

        # เช็คว่าชื่อถูกเปลี่ยนจริงไหม
        user.refresh_from_db()
        self.assertEqual(user.username, "updateduser")

    # ✅ 9) ทดสอบ logout
    def test_logout(self):
        user = User.objects.create_user(username="testuser", password="StrongPass123!")
        self.client.login(username="testuser", password="StrongPass123!")

        response = self.client.get(reverse("logout"))

        # logout แล้วต้องเด้งกลับ home
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
