from django.db.models import TextChoices


class Statuses(TextChoices):
    REMOVED = 'REMOVED'
    ENABLED = 'ENABLED'
