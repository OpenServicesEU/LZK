import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from . import models


class AbilityTable(tables.Table):
    levels = tables.TemplateColumn(
        verbose_name=_("Levels"),
        template_name="LZK/ability/includes/levels.html",
        orderable=False,
    )
    link = tables.TemplateColumn(
        verbose_name=_("Link"),
        template_name="LZK/ability/includes/link.html",
        orderable=False,
    )

    class Meta:
        model = models.Ability
        fields = ("name", "depth")


class AbilityFeedbackTable(tables.Table):
    levels = tables.TemplateColumn(
        verbose_name=_("Levels"),
        template_name="LZK/ability/includes/levels.html",
        orderable=False,
    )
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/comment/table/ability.html",
        orderable=False,
    )

    class Meta:
        model = models.Ability
        fields = ("name",)


class SymptomTable(tables.Table):
    link = tables.TemplateColumn(
        verbose_name=_("Link"),
        template_name="LZK/symptom/includes/link.html",
        orderable=False,
    )

    class Meta:
        model = models.Symptom
        fields = ("name",)


class SymptomFeedbackTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/comment/table/symptom.html",
        orderable=False,
    )

    class Meta:
        model = models.Symptom
        fields = ("name",)


class CompetenceLevelTable(tables.Table):
    activities = tables.TemplateColumn(
        verbose_name=_("Activities"),
        template_name="LZK/competence_level/activities.html",
        orderable=False,
    )

    class Meta:
        model = models.CompetenceLevel
        fields = ("name",)


class SkillTable(tables.Table):
    name = tables.Column(verbose_name=_("Skill"))
    link = tables.TemplateColumn(
        verbose_name=_("Link"),
        template_name="LZK/skill/includes/link.html",
        orderable=False,
    )

    class Meta:
        model = models.Skill
        fields = (
            "name",
            "link",
        )


class SkillFeedbackTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name=_("Actions"),
        template_name="LZK/comment/table/skill.html",
        orderable=False,
    )

    class Meta:
        model = models.Skill
        fields = ("name",)
