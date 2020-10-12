import django_filters
from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.utils.translation import gettext as _

from .. import models


class FeedbackFilter(django_filters.FilterSet):
    class Meta:
        model = models.Feedback
        fields = {
            "university": ["exact"],
        }

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


class AbilityCommentFilter(django_filters.FilterSet):
    ability = django_filters.CharFilter(
        "ability__name", "icontains", label=_("Ability")
    )
    comment = django_filters.CharFilter("comment", "icontains", label=_("Comment"))

    class Meta:
        model = models.AbilityComment
        fields = tuple()

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
                StrictButton(
                    _("Apply"), type="submit", css_class="btn btn-primary btn-block"
                ),
            )
        )
        form.helper = helper
        return form


class SymptomCommentFilter(django_filters.FilterSet):
    symptom = django_filters.CharFilter(
        "symptom__name", "icontains", label=_("Symptom")
    )
    comment = django_filters.CharFilter("comment", "icontains", label=_("Comment"))

    class Meta:
        model = models.SymptomComment
        fields = tuple()

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
                StrictButton(
                    _("Apply"), type="submit", css_class="btn btn-primary btn-block"
                ),
            )
        )
        form.helper = helper
        return form


class SkillCommentFilter(django_filters.FilterSet):
    skill = django_filters.CharFilter("skill__name", "icontains", label=_("Skill"))
    comment = django_filters.CharFilter("comment", "icontains", label=_("Comment"))

    class Meta:
        model = models.SkillComment
        fields = tuple()

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
                StrictButton(
                    _("Apply"), type="submit", css_class="btn btn-primary btn-block"
                ),
            )
        )
        form.helper = helper
        return form
