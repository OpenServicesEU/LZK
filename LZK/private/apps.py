from django.apps import AppConfig
from django.core.checks import Tags, register
from django.utils.translation import gettext_lazy as _

from .checks import check_email_from


class LZKPrivateConfig(AppConfig):
    name = "LZK.private"
    verbose_name = _("Lernzielkatalog (Private)")

    def ready(self):
        super().ready()
        register(Tags.admin)(check_email_from)
