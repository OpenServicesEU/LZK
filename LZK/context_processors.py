from . import models


def navigation(request):
    return {
        "subjects": models.Subject.objects.all(),
    }
