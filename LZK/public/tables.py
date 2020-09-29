import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .. import models


class ObjectiveCommentTable(tables.Table):
    actions = tables.TemplateColumn(
        verbose_name=_('Actions'),
        template_name='LZK/public/comment/actions.html',
        orderable=False
    )

    class Meta:
        model = models.Objective
        fields = ("name",)


class ObjectiveSubjectTable(tables.Table):
    pk = tables.Column(
        linkify=("public:objective-subject-detail", {"pk": tables.A("pk")})
    )

    class Meta:
        model = models.Subject
        fields = ("pk", "name",)


class ObjectiveTable(tables.Table):
    levels = tables.TemplateColumn(
        verbose_name=_('Levels'),
        template_name='LZK/public/objective/levels.html',
        orderable=False
    )
    subjects = tables.TemplateColumn(
        verbose_name=_('Subjects'),
        template_name='LZK/public/objective/subjects.html',
        orderable=False
    )

    class Meta:
        model = models.Objective
        fields = ("name", "depth")


class SymptomSubjectTable(tables.Table):
    pk = tables.Column(
        linkify=("public:symptom-subject-detail", {"pk": tables.A("pk")})
    )

    class Meta:
        model = models.Subject
        fields = ("pk", "name",)


class SymptomTable(tables.Table):
    subjects = tables.TemplateColumn(
        verbose_name=_('Subjects'),
        template_name='LZK/public/symptom/subjects.html',
        orderable=False
    )

    class Meta:
        model = models.Symptom
        fields = ("name",)


class CompetenceLevelTable(tables.Table):
    activities = tables.TemplateColumn(
        verbose_name=_('Activities'),
        template_name='LZK/public/competence_level/activities.html',
        orderable=False
    )

    class Meta:
        model = models.CompetenceLevel
        fields = ("name",)


class SkillTable(tables.Table):

    class Meta:
        model = models.Skill
        fields = ("name",)
