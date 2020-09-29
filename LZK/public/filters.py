import django_filters

from .. import models


class ObjectiveFilter(django_filters.FilterSet):
    class Meta:
        model = models.Objective
        fields = ["name", "depth"]


class SymptomFilter(django_filters.FilterSet):
    class Meta:
        model = models.Symptom
        fields = ["name"]


class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = models.Subject
        fields = ["name"]


class SubjectObjectiveFilter(django_filters.FilterSet):
    class Meta:
        model = models.Objective
        fields = ["name"]


class SkillFilter(django_filters.FilterSet):
    class Meta:
        model = models.Skill
        fields = ["name"]
