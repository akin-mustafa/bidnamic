from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework.test import APIRequestFactory

from bidnamic.users.tests.factory import UserFactory


class UrlsTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.rf = APIRequestFactory()

    def test_detail(self) -> None:
        self.assertEqual(
            reverse("users:detail", kwargs={"username": self.user.username}),
            f"/users/{self.user.username}/",
        )
        self.assertEqual(
            resolve(f"/users/{self.user.username}/").view_name, "users:detail"
        )

    def test_update(self) -> None:
        self.assertEqual(reverse("users:update"), "/users/update/")
        self.assertEqual(resolve("/users/update/").view_name, "users:update")

    def test_redirect(self) -> None:
        self.assertEqual(reverse("users:redirect"), "/users/redirect/")
        self.assertEqual(resolve("/users/redirect/").view_name, "users:redirect")
