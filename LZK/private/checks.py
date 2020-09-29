from django.core.checks import Error

from .conf import settings


def check_email_from(app_configs, **kwargs):
    if not getattr(settings, "LZK_EMAIL_FROM", None):
        yield Error(
            "No default sender specified in LZK_EMAIL_FROM",
            hint="Make sure to define a default sender in settings.LZK_EMAIL_FROM.",
            obj=settings,
            id=f"{__package__}.E001",
        )
