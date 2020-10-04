from django.conf import settings


def login_url(request):
    return {
        "login_url": settings.LOGIN_URL,
    }
