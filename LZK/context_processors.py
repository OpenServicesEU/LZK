from .conf import settings
from . import models


def login_url(request):
    return {
        "login_url": settings.LOGIN_URL,
    }


def copyright(request):
    return {
        "copyright": settings.LZK_COPYRIGHT,
    }


def top_downloads(request):
    return {
        "top_downloads": models.Download.objects.filter(active=True, top=True),
    }
