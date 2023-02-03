import django_filters
from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.utils.translation import gettext as _

from . import models


class AbilityExtendedFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Ability"))

    class Meta:
        model = models.Ability
        fields = (
            "name",
            "depth",
            "subjects",
            "study_field",
        )

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.declared_fields)
        helper = FormHelper(form)
        helper.form_method = "post"
        helper.form_action = "."
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                StrictButton(_("Generate public URL"), type="submit", css_class="btn btn-primary"),
                css_class="d-flex flex-row-reverse",
            )
        )
        form.helper = helper
        return form


class AbilityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Ability"))

    class Meta:
        model = models.Ability
        fields = (
            "name",
            "depth",
        )

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.declared_fields)
        helper = FormHelper(form)
        helper.form_method = "get"
        helper.form_action = "."
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                StrictButton(_("Apply"), type="submit", css_class="btn btn-primary"),
                css_class="d-flex flex-row-reverse",
            )
        )
        form.helper = helper
        return form


class SymptomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Symptom"))

    class Meta:
        model = models.Symptom
        fields = ("name",)

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.declared_fields)
        helper = FormHelper(form)
        helper.form_method = "get"
        helper.form_action = "."
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                StrictButton(_("Apply"), type="submit", css_class="btn btn-primary"),
                css_class="d-flex flex-row-reverse",
            )
        )
        form.helper = helper
        return form


class SkillFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Skill"))

    class Meta:
        model = models.Skill
        fields = ("name",)

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.declared_fields)
        helper = FormHelper(form)
        helper.form_method = "get"
        helper.form_action = "."
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                StrictButton(_("Apply"), type="submit", css_class="btn btn-primary"),
                css_class="d-flex flex-row-reverse",
            )
        )
        form.helper = helper
        return form
