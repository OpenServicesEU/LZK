from .conf import settings


def login_url(request):
    return {
        "login_url": settings.LOGIN_URL,
    }


def copyright(request):
    return {
        "copyright": settings.LZK_COPYRIGHT,
    }
