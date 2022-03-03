import logging

from crispy_forms.bootstrap import FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count, Q
from django.http import Http404
from django.urls import reverse_lazy as reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterMixin, FilterView
from django_tables2.views import SingleTableMixin
from rest_framework import viewsets
from haystack.generic_views import SearchView as BaseSearchView

from . import filters, forms, models, tables, serializers
from .layout import IconButton

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "LZK/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slides"] = models.Slide.objects.filter(active=True)
        context["universities"] = models.University.objects.all()
        context["news"] = models.News.objects.filter(
            Q(active=None) | Q(active__lte=timezone.now())
        )[:10]
        context["downloads"] = models.Download.objects.filter(active=True)
        context["texts"] = models.Text.objects.filter(placement=models.Text.HOMEPAGE)
        return context


class AboutView(TemplateView):
    template_name = "LZK/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texts"] = models.Text.objects.filter(placement=models.Text.ABOUT)
        return context


class AbilityListView(SingleTableMixin, FilterView):
    model = models.Ability
    table_class = tables.AbilityTable
    template_name = "LZK/ability/list.html"
    filterset_class = filters.AbilityFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texts"] = models.Text.objects.filter(placement=models.Text.ABILITIES)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(public=False).order_by("name")


class AbilityDetailView(DetailView):
    model = models.Ability
    template_name = "LZK/ability/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(public=False)


class SymptomListView(SingleTableMixin, FilterView):
    model = models.Symptom
    table_class = tables.SymptomTable
    template_name = "LZK/symptom/list.html"
    filterset_class = filters.SymptomFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texts"] = models.Text.objects.filter(placement=models.Text.SYMPTOMS)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(public=False).order_by("name")


class SymptomDetailView(DetailView):
    model = models.Symptom
    template_name = "LZK/symptom/detail.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(public=False)


class CompetenceLevelView(ListView):
    model = models.CompetenceLevel
    template_name = "LZK/competence_level/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["texts"] = models.Text.objects.filter(placement=models.Text.SKILLS)
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(activity_count=Count("activity")).filter(
            activity_count__gt=0
        )


class ActivityView(SingleTableMixin, SingleObjectMixin, FilterView):
    model = models.Activity
    table_class = tables.SkillTable
    template_name = "LZK/activity/list.html"
    filterset_class = filters.SkillFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_table_data(self):
        return self.object.skill_set.all()

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["queryset"] = self.object.skill_set.all()
        return kwargs


class SkillDetailView(DetailView):
    model = models.Skill
    template_name = "LZK/skill/detail.html"


class SubjectView(SingleTableMixin, SingleObjectMixin, FilterView):
    model = models.Subject
    table_class = tables.AbilityTable
    template_name = "LZK/subject/list.html"
    filterset_class = filters.AbilityFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_table_data(self):
        return self.object.ability_set.all()

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["queryset"] = self.object.ability_set.all()
        return kwargs


class FeedbackTokenMixin(UserPassesTestMixin):
    def test_func(self):
        token = self.request.GET.get("token", self.request.session.get("token"))
        if not token:
            return False
        try:
            feedback = models.Feedback.objects.get(secret=token)
        except models.Feedback.DoesNotExist:
            return False
        self.request.session["token"] = token
        setattr(self, "feedback", feedback)
        return True


class CommentMixin(object):
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            obj = self.get_commentables().get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": self.comment._meta.verbose_name}
            )
        comment, created = self.model.objects.get_or_create(
            **{
                self.relation: obj,
                "feedback": self.feedback,
            }
        )
        if created:
            logger.info(f"Created new comment by {self.feedback} for {obj}")
        return comment


class FeedbackView(FeedbackTokenMixin, UpdateView):
    model = models.Feedback
    template_name = "LZK/feedback/index.html"
    fields = ("notes",)
    success_url = reverse("feedback")

    def get_object(self):
        return self.feedback

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.base_fields)
        helper = FormHelper(form)
        helper.form_method = "post"
        helper.form_action = "."
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                IconButton(
                    "fa fa-floppy-o",
                    _("Save"),
                    type="submit",
                    css_class="btn btn-primary btn-block",
                ),
            ),
        )
        form.helper = helper
        return form


class AbilityFeedbackView(
    FeedbackTokenMixin, SingleTableMixin, SingleObjectMixin, FilterView
):
    model = models.Subject
    table_class = tables.AbilityFeedbackTable
    template_name = "LZK/feedback/abilities.html"
    filterset_class = filters.AbilityFilter
    paginate_by = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.feedback.subjects.annotate(ability_count=Count("ability")).filter(
            ability_count__gt=0
        )

    def get_table(self):
        table = super().get_table()
        table.columns["actions"].column.extra_context["subject"] = self.object
        return table

    def get_table_data(self):
        return self.object.ability_set.all()


class AbilityCommentView(FeedbackTokenMixin, CommentMixin, UpdateView):
    model = models.AbilityComment
    template_name = "LZK/comment/ability.html"
    fields = ("comment",)
    comment = models.Ability
    relation = "ability"

    def get_commentables(self):
        return self.comment.objects.filter(subjects__in=self.feedback.subjects.all())

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.base_fields)
        helper = FormHelper(form)
        helper.form_method = "post"
        action = reverse("comment-ability", kwargs={"pk": self.object.ability.pk})
        subject = self.request.GET.get("subject")
        if subject:
            helper.form_action = f"{action}?subject={subject}"
        else:
            helper.form_action = action
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                IconButton(
                    "fa fa-floppy-o",
                    _("Save"),
                    type="submit",
                    css_class="btn btn-primary btn-block",
                ),
            ),
        )
        form.helper = helper
        return form

    def get_success_url(self):
        subject = self.request.GET.get("subject")
        if subject:
            return reverse("feedback-ability", kwargs={"pk": subject})
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.request.GET.get("subject")
        if subject:
            context["subject"] = subject
        return context


class SymptomFeedbackView(
    FeedbackTokenMixin, SingleTableMixin, SingleObjectMixin, FilterView
):
    model = models.Subject
    table_class = tables.SymptomFeedbackTable
    template_name = "LZK/feedback/symptoms.html"
    filterset_class = filters.SymptomFilter
    paginate_by = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.feedback.subjects.annotate(symptom_count=Count("symptom")).filter(
            symptom_count__gt=0
        )

    def get_table_data(self):
        return self.object.symptom_set.all()


class SymptomCommentView(FeedbackTokenMixin, CommentMixin, UpdateView):
    model = models.SymptomComment
    template_name = "LZK/comment/symptom.html"
    fields = ("comment",)
    comment = models.Symptom
    relation = "symptom"

    def get_commentables(self):
        return self.comment.objects.filter(subjects__in=self.feedback.subjects.all())

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.base_fields)
        helper = FormHelper(form)
        helper.form_method = "post"
        action = reverse("comment-symptom", kwargs={"pk": self.object.symptom.pk})
        subject = self.request.GET.get("subject")
        if subject:
            helper.form_action = f"{action}?subject={subject}"
        else:
            helper.form_action = action
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                IconButton(
                    "fa fa-floppy-o",
                    _("Save"),
                    type="submit",
                    css_class="btn btn-primary btn-block",
                ),
            ),
        )
        form.helper = helper
        return form

    def get_success_url(self):
        subject = self.request.GET.get("subject")
        if subject:
            return reverse("feedback-symptom", kwargs={"pk": subject})
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.request.GET.get("subject")
        if subject:
            context["subject"] = subject
        return context


class SkillFeedbackView(
    FeedbackTokenMixin, SingleTableMixin, SingleObjectMixin, FilterView
):
    model = models.Activity
    table_class = tables.SkillFeedbackTable
    template_name = "LZK/feedback/skills.html"
    filterset_class = filters.SkillFilter
    paginate_by = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.feedback.activities.annotate(skill_count=Count("skill")).filter(
            skill_count__gt=0
        )

    def get_table(self):
        table = super().get_table()
        table.columns["actions"].column.extra_context["activity"] = self.object
        return table

    def get_table_data(self):
        return self.object.skill_set.all()


class SkillCommentView(FeedbackTokenMixin, CommentMixin, UpdateView):
    model = models.SkillComment
    template_name = "LZK/comment/skill.html"
    fields = ("comment",)
    comment = models.Skill
    relation = "skill"

    def get_commentables(self):
        return self.comment.objects.filter(activity__in=self.feedback.activities.all())

    def get_form_class(self):
        form = super().get_form_class()
        if not hasattr(form, "fields"):
            setattr(form, "fields", form.base_fields)
        helper = FormHelper(form)
        helper.form_method = "post"
        action = reverse("comment-skill", kwargs={"pk": self.object.skill.pk})
        activity = self.request.GET.get("activity")
        if activity:
            helper.form_action = f"{action}?activity={activity}"
        else:
            helper.form_action = action
        helper.html5_required = True
        helper.layout = Layout(
            *form.fields.keys(),
            FormActions(
                IconButton(
                    "fa fa-floppy-o",
                    _("Save"),
                    type="submit",
                    css_class="btn btn-primary btn-block",
                ),
            ),
        )
        form.helper = helper
        return form

    def get_success_url(self):
        activity = self.request.GET.get("activity")
        if activity:
            return reverse("feedback-skill", kwargs={"pk": activity})
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self.request.GET.get("activity")
        if activity:
            context["activity"] = activity
        return context


class SearchView(BaseSearchView):
    template_name = "LZK/search.html"
    results_per_page = 10


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Skill.objects.all()
    serializer_class = serializers.SkillSerializer
    filterset_fields = ["clinical_traineeship_checklist", "activity"]


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
