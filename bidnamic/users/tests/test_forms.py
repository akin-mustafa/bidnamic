from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from bidnamic.users.forms import UserAdminCreationForm
from bidnamic.users.tests.factory import UserFactory


class TestUserAdminForms(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_admin_create_form_username_validation_error_msg(self):

        form = UserAdminCreationForm(
            {
                "username": self.user.username,
                "password1": self.user.password,
                "password2": self.user.password,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue("username" in form.errors)
        self.assertEqual(
            form.errors["username"][0], _("This username has already been taken.")
        )
