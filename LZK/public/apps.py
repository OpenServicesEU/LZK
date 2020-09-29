from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LZKPublicConfig(AppConfig):
    name = "public"
    verbose_name = _("Lernzielkatalog Public)")
