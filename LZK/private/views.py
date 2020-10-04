import logging
from crispy_forms.bootstrap import FormActions, StrictButton
from psqlextra.query import ConflictAction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from psqlextra.util import postgres_manager
from itertools import islice

from openpyxl import load_workbook
from django.urls import reverse_lazy as reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.views.generic import TemplateView, FormView
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext_lazy as _
from braces.views import SuperuserRequiredMixin


from ..mixins import FilterFormHelperMixin
from .. import models
from .conf import settings
from . import forms, tables, filters

logger = logging.getLogger(__name__)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "LZK/private/index.html"


class ImportView(LoginRequiredMixin, SuperuserRequiredMixin, FormView):
    template_name = "LZK/private/import.html"
    form_class = forms.ImportForm
    extra_context = {
        "sheets": [
            settings.LZK_IMPORT_SHEET_ACRONYMS,
            settings.LZK_IMPORT_SHEET_UFIDS,
            settings.LZK_IMPORT_SHEET_OBJECTIVES,
        ]
    }
    success_url = reverse("private:index")

    def form_valid(self, form):
        wb = load_workbook(
            form.cleaned_data.get("file"),
            read_only=True,
            data_only=True,
            keep_links=False,
        )
        acronyms = {
            k.value.upper(): v.value
            for v, k, *_ in wb.get_sheet_by_name(settings.LZK_IMPORT_SHEET_ACRONYMS)
        }
        ufid_sheet = wb.get_sheet_by_name(settings.LZK_IMPORT_SHEET_UFIDS)
        ufid_data = (
            {"id": x[2].value, "name": x[3].value}
            for x in islice(ufid_sheet.iter_rows(), 1, None)
        )
        models.UFID.objects.on_conflict(["id"], ConflictAction.UPDATE).bulk_insert(
            ufid_data
        )

        objective_sheet = wb.get_sheet_by_name(settings.LZK_IMPORT_SHEET_OBJECTIVES)
        objective_data = list()
        level_data = dict()
        activity_data = dict()
        cl_data = dict()
        cl_activity_map = dict()
        skill_data = list()
        skill_activity_map = dict()
        subject_data = dict()
        system_data = dict()
        study_field_data = dict()
        objective_level_data = list()
        objective_subject_data = list()
        objective_system_data = list()
        objective_ufid_data = list()
        objective_study_field_data = dict()
        symptom_data = list()
        symptom_subject_data = list()
        for row in islice(objective_sheet.iter_rows(), 1, None):
            if row[10].value.strip().lower() == settings.LZK_IMPORT_VALUE_TRUE.lower():
                # Symptom
                symptom_data.append(
                    {
                        "pk": row[0].value,
                        "name": row[1].value.strip(),
                    }
                )
                # Subjects
                if row[7].value:
                    for s in filter(
                        bool, map(lambda s: s.strip(), row[7].value.split(","))
                    ):
                        if s.upper() not in subject_data:
                            subject_data[s.upper()] = {"name": acronyms.get(s.upper(), s)}
                        symptom_subject_data.append(
                            {"symptom_id": row[0].value, "subject_id": s.upper()}
                        )
            elif bool(row[11].value):
                # Competence levels
                if row[3].value and row[6].value:
                    cl = row[3].value.strip()
                    if cl.upper() not in cl_data:
                        cl_data[cl.upper()] = {
                            "name": acronyms.get(cl.upper(), cl),
                        }
                    act = row[6].value.strip()
                    if act not in activity_data:
                        activity_data[act] = cl.upper()
                    skill_data.append(
                        {
                            "pk": row[0].value,
                            "name": row[1].value.strip(),
                        }
                    )
                    skill_activity_map[row[0].value] = act
            else:
                objective_data.append(
                    {
                        "pk": row[0].value,
                        "name": row[1].value.strip(),
                        "depth": row[2].value,
                        "subject_related": row[9].value.strip().lower()
                        == settings.LZK_IMPORT_VALUE_TRUE.lower(),
                    }
                )
                # Levels
                if row[3].value:
                    for l in map(lambda l: l.strip(), row[3].value.split(",")):
                        if l.upper() not in level_data:
                            level_data[l.upper()] = {"name": acronyms.get(l.upper(), l)}
                        objective_level_data.append(
                            {"objective_id": row[0].value, "level_id": l.upper()}
                        )
                # Subjects
                if row[7].value:
                    for s in filter(
                        bool, map(lambda s: s.strip(), row[7].value.split(","))
                    ):
                        if s.upper() not in subject_data:
                            subject_data[s.upper()] = {"name": acronyms.get(s.upper(), s)}
                        objective_subject_data.append(
                            {"objective_id": row[0].value, "subject_id": s.upper()}
                        )
                # Systems
                if row[12].value:
                    for s in map(lambda s: s.strip(), row[12].value.split(",")):
                        if s.upper() not in system_data:
                            system_data[s.upper()] = {"name": acronyms.get(s.upper(), s)}
                        objective_system_data.append(
                            {"objective_id": row[0].value, "system_id": s.upper()}
                        )
                # UFIDs
                if row[15].value:
                    if isinstance(row[15].value, int):
                        values = [row[15].value]
                    elif isinstance(row[15].value, float):
                        values = map(
                            lambda u: int(u.strip()),
                            filter(bool, str(row[15].value).split(".")),
                        )
                    else:
                        values = map(
                            lambda u: int(u.strip()), filter(bool, row[15].value.split(","))
                        )
                    for u in values:
                        objective_ufid_data.append(
                            {"objective_id": row[0].value, "ufid_id": u}
                        )
                # Study field
                if row[16].value:
                    sf = row[16].value.strip()
                    if sf.upper() not in study_field_data:
                        study_field_data[sf.upper()] = {
                            "name": acronyms.get(sf.upper(), sf)
                        }
                    objective_study_field_data[row[0].value] = sf.upper()

        models.StudyField.objects.on_conflict(
            ["pk"], ConflictAction.UPDATE
        ).bulk_insert(({**v, **{"pk": k}} for k, v in study_field_data.items()))

        objective_data_update = [
            {
                **o,
                **{
                    "study_field_id": objective_study_field_data.get(o.get("pk")),
                },
            }
            for o in objective_data
            if o.get("pk") in objective_study_field_data
        ]

        for k, v in cl_data.items():
            models.CompetenceLevel.objects.get_or_create(pk=k, defaults=v)

        models.Activity.objects.on_conflict(
            ["name"], ConflictAction.UPDATE
        ).bulk_insert(({"name": k, "competence_level_id": v} for k, v in activity_data.items()))
        activities_pk = {a.name: a.pk for a in models.Activity.objects.all()}

        skill_data_update = [
            {
                **s,
                **{
                    "activity_id": activities_pk.get(
                        skill_activity_map.get(s.get("pk"))
                    ),
                },
            }
            for s in skill_data
            if s.get("pk") in skill_activity_map
        ]

        models.Skill.objects.on_conflict(
            ["pk"], ConflictAction.UPDATE
        ).bulk_insert(skill_data_update)

        objs = models.Objective.objects.on_conflict(
            ["pk"], ConflictAction.UPDATE
        ).bulk_insert(objective_data_update)
        #models.Objective.subjects.through.objects.filter(
        #    objective__pk__in=pks
        #).delete()

        syms = models.Symptom.objects.on_conflict(
            ["pk"], ConflictAction.UPDATE
        ).bulk_insert(symptom_data)
        #models.Symptom.subjects.through.objects.filter(
        #    symptom__pk__in=pks
        #).delete()

        models.Subject.objects.on_conflict(["pk"], ConflictAction.UPDATE).bulk_insert(
            ({**v, **{"pk": k}} for k, v in subject_data.items())
        )

        with postgres_manager(models.Objective.subjects.through) as manager:
            manager.get_queryset().bulk_insert(objective_subject_data)

        with postgres_manager(models.Symptom.subjects.through) as manager:
            manager.get_queryset().bulk_insert(symptom_subject_data)

        models.Level.objects.on_conflict(["pk"], ConflictAction.UPDATE).bulk_insert(
            ({**v, **{"pk": k}} for k, v in level_data.items())
        )
        models.System.objects.on_conflict(["pk"], ConflictAction.UPDATE).bulk_insert(
            ({**v, **{"pk": k}} for k, v in system_data.items())
        )

        #models.Objective.levels.through.objects.filter(
        #    objective__pk__in=pks
        #).delete()
        with postgres_manager(models.Objective.levels.through) as manager:
            manager.get_queryset().bulk_insert(objective_level_data)


        #models.Objective.systems.through.objects.filter(
        #    objective__pk__in=pks
        #).delete()
        with postgres_manager(models.Objective.systems.through) as manager:
            manager.get_queryset().bulk_insert(objective_system_data)

        #models.Objective.ufids.through.objects.filter(
        #    objective__pk__in=pks
        #).delete()
        with postgres_manager(models.Objective.ufids.through) as manager:
            manager.get_queryset().bulk_insert(objective_ufid_data)

        return super().form_valid(form)


class ListObjectiveView(LoginRequiredMixin, ListView):
    model = models.Objective
    paginate_by = 50
    template_name = "LZK/private/objective/list.html"


class ListFeedbackView(
    LoginRequiredMixin, SingleTableMixin, FilterFormHelperMixin, FilterView
):
    model = models.Feedback
    template_name = "LZK/private/feedback/list.html"
    table_class = tables.FeedbackTable
    filterset_class = filters.FeedbackFilter

    def get_filterset_formhelper(self, form):
        helper = FormHelper(form)
        helper.form_action = "."
        helper.form_method = "GET"
        helper.html5_required = True
        # import pudb; pu.db
        helper.layout = Layout(
            Fieldset(
                "Filter",
                *helper.layout.fields,
                FormActions(
                    StrictButton("Filter", type="submit", css_class="btn-primary"),
                    css_class="form-group",
                ),
            )
        )
        return helper


class CreateFeedbackView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Feedback
    form_class = forms.FeedbackForm
    template_name = "LZK/private/feedback/create.html"
    success_url = reverse("private:feedback-list")
    permission_required = 'LZK.add_feedback'

    def form_valid(self, form):
        response = super().form_valid(form)
        plaintext = get_template("LZK/private/email/feedback.txt")
        html = get_template("LZK/private/email/feedback.html")
        for contact in self.object.university.contact_set.all():
            logger.info(f"Sending mail: {self.object} to {contact}")
            d = {
                "contact": contact,
                "object": self.object,
                "request": self.request,
            }
            msg = EmailMultiAlternatives(
                _("LZK: Request for feedback"),
                plaintext.render(d),
                settings.LZK_EMAIL_FROM,
                [contact.email],
            )
            msg.attach_alternative(html.render(d), "text/html")
            msg.send()
        return response


class DetailFeedbackView(LoginRequiredMixin, PermissionRequiredMixin, SingleTableMixin, DetailView):
    model = models.Feedback
    template_name = "LZK/private/feedback/detail.html"
    table_class = tables.CommentTable
    permission_required = 'LZK.view_feedback'

    def get_table_data(self):
        return self.object.comment_set.all()
