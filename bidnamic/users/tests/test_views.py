from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseRedirect
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from bidnamic.users.forms import UserAdminChangeForm
from bidnamic.users.tests.factory import UserFactory
from bidnamic.users.views import UserRedirectView, UserUpdateView, user_detail_view


class UserDetailViewTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.rf = APIRequestFactory()

    def test_get_success_url(self):
        view = UserUpdateView()
        request = self.rf.get("/fake-url/")
        request.user = self.user

        view.request = request

        self.assertEqual(view.get_success_url(), f"/users/{self.user.username}/")

    def test_get_object(self):
        view = UserUpdateView()
        request = self.rf.get("/fake-url/")
        request.user = self.user

        view.request = request

        self.assertEqual(self.user, view.get_object())

    def test_form_valid(self):
        view = UserUpdateView()
        request = self.rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(None).process_request(request)
        MessageMiddleware(None).process_request(request)
        request.user = self.user

        view.request = request

        # Initialize the form
        form = UserAdminChangeForm()
        form.cleaned_data = []
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        self.assertEqual(messages_sent, ["Information successfully updated"])


class TestUserRedirectView(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.rf = APIRequestFactory()

    def test_get_redirect_url(self):
        view = UserRedirectView()
        request = self.rf.get("/fake-url")
        request.user = self.user

        view.request = request

        self.assertEqual(view.get_redirect_url(), f"/users/{self.user.username}/")


class TestUserDetailView(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.rf = APIRequestFactory()

    def test_authenticated(self):
        request = self.rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, username=self.user.username)

        self.assertEqual(response.status_code, 200)

    def test_not_authenticated(self):
        request = self.rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, username=self.user.username)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
