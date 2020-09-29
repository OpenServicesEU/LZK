from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.core.checks import register, Tags

from .checks import check_email_from


class LZKPrivateConfig(AppConfig):
    name = "private"
    verbose_name = _("Lernzielkatalog (Private)")

    def ready(self):
        super().ready()
        register(Tags.admin)(check_email_from)
