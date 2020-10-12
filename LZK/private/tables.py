import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .. import models


class FeedbackTable(tables.Table):
    stats = tables.TemplateColumn(
        verbose_name=_("Comments"),
        template_name="LZK/private/feedback/table/stats.html",
        orderable=False,
    )
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/private/feedback/table/actions.html",
        orderable=False,
    )

    class Meta:
        model = models.Feedback
        fields = ("university",)


class AbilityCommentTable(tables.Table):
    text = tables.TemplateColumn(
        verbose_name=_("Ability"),
        template_name="LZK/private/comment/ability/table/text.html",
        orderable=True,
    )
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/private/comment/ability/table/actions.html",
        orderable=False,
    )

    class Meta:
        model = models.AbilityComment
        fields = (
            "text",
            "actions",
        )


class SymptomCommentTable(tables.Table):
    text = tables.TemplateColumn(
        verbose_name=_("Ability"),
        template_name="LZK/private/comment/symptom/table/text.html",
        orderable=True,
    )
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/private/comment/symptom/table/actions.html",
        orderable=False,
    )

    class Meta:
        model = models.SymptomComment
        fields = (
            "text",
            "actions",
        )


class SkillCommentTable(tables.Table):
    text = tables.TemplateColumn(
        verbose_name=_("Ability"),
        template_name="LZK/private/comment/skill/table/text.html",
        orderable=True,
    )
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/private/comment/skill/table/actions.html",
        orderable=False,
    )

    class Meta:
        model = models.SkillComment
        fields = (
            "text",
            "actions",
        )
