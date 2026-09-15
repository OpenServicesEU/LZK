from django.utils import translation


class LanguageSelectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.GET.get("language")
        response = self.get_response(request)
        if language is not None:
            translation.activate(language)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
