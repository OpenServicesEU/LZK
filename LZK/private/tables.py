import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .. import models


class FeedbackTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='LZK/private/feedback/actions.html',
        orderable=False
    )

    class Meta:
        model = models.Feedback
        fields = (
            "university",
            "subject",
        )


class CommentTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='LZK/private/comment/actions.html',
        orderable=False
    )

    class Meta:
        model = models.Comment
        fields = (
            "objective",
            "accepted",
        )
