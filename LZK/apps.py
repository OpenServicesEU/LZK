from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LZKConfig(AppConfig):
    name = "LZK"
    verbose_name = _("Lernzielkatalog")
    default_auto_field = "django.db.models.BigAutoField"
