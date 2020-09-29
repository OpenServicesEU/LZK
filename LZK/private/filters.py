import django_filters

from .. import models


class FeedbackFilter(django_filters.FilterSet):
    class Meta:
        model = models.Feedback
        fields = {
            "university": ["exact"],
            "university__name": ["icontains"],
            "subject": ["exact"],
            "subject__name": ["icontains"],
        }
