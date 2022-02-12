from django.utils import translation


class LanguageSelectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.GET.get("language")
        if language is not None:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
        response = self.get_response(request)
        return response
