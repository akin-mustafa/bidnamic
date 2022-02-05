from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from core.models.base_models import BaseAbstractModel


class User(BaseAbstractModel, AbstractUser):
    """
    Default custom user model for Bidnamic.
    """

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})