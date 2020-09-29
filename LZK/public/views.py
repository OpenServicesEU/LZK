import logging
from haystack.generic_views import SearchView as BaseSearchView
from django.db.models import Q
from django_filters.views import FilterView, FilterMixin
from django_tables2.views import SingleTableMixin
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.http import Http404
from django.urls import reverse_lazy as reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import UserPassesTestMixin

from .. import models
from . import forms, tables, filters


logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "LZK/public/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slides"] = models.Slide.objects.filter(active=True)
        context["universities"] = models.University.objects.all()
        context["news"] = models.News.objects.filter(Q(active=None) | Q(active__lte=timezone.now()))[:10]
        return context


class ObjectiveSubjectListView(SingleTableMixin, FilterView):
    model = models.Subject
    table_class = tables.ObjectiveSubjectTable
    template_name = "LZK/public/objective/subject.html"
    filterset_class = filters.SubjectFilter
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(objective=None).order_by("name")


class ObjectiveSubjectDetailView(SingleTableMixin, FilterMixin, DetailView):
    model = models.Subject
    table_class = tables.ObjectiveTable
    template_name = "LZK/public/objective/list.html"
    filterset_class = filters.ObjectiveFilter
    paginate_by = 10

    def get_table_data(self):
        return self.object.objective_set.exclude(depth=None)#.filter(public=True)


class SymptomSubjectListView(SingleTableMixin, FilterView):
    model = models.Subject
    table_class = tables.SymptomSubjectTable
    template_name = "LZK/public/symptom/subject.html"
    filterset_class = filters.SubjectFilter
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(symptom=None).order_by("name")


class SymptomSubjectDetailView(SingleTableMixin, FilterMixin, DetailView):
    model = models.Subject
    table_class = tables.SymptomTable
    template_name = "LZK/public/symptom/list.html"
    filterset_class = filters.SymptomFilter
    paginate_by = 10

    def get_table_data(self):
        return self.object.objective_set.exclude(depth=None)#.filter(public=True)


class CompetenceLevelView(SingleTableMixin, ListView):
    model = models.CompetenceLevel
    table_class = tables.CompetenceLevelTable
    template_name = "LZK/public/competence_level/list.html"


class ActivityView(SingleTableMixin, FilterMixin, DetailView):
    model = models.Activity
    table_class = tables.SkillTable
    template_name = "LZK/public/activity/list.html"
    filterset_class = filters.SkillFilter
    paginate_by = 10

    def get_table_data(self):
        return self.object.skill_set.all()


class FeedbackTokenMixin(UserPassesTestMixin):
    def test_func(self):
        token = self.request.GET.get("token", self.request.session.get("token"))
        if not token:
            return False
        try:
            feedback = models.Feedback.objects.get(secret=token)
        except models.Feedback.DoesNotExist:
            return False
        else:
            self.request.session["token"] = token
            setattr(self, "feedback", feedback)
        return True


class CommentView(FeedbackTokenMixin, SingleTableMixin, FilterView):
    model = models.Objective
    table_class = tables.ObjectiveCommentTable
    template_name = "LZK/public/comment/list.html"
    filterset_class = filters.ObjectiveFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(subjects=self.feedback.subject)


class ObjectiveCommentView(FeedbackTokenMixin, UpdateView):
    model = models.Comment
    template_name = "LZK/public/comment/form.html"
    form_class = forms.CommentForm
    success_url = reverse("public:comment")

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(feedback=self.feedback)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        try:
            obj = models.Objective.objects.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": models.Objective._meta.verbose_name}
            )
        feedback, created = queryset.get_or_create(
            objective=obj, feedback=self.feedback
        )
        if created:
            logger.info(f"Created new comment by {self.feedback} for {obj}")
        return feedback


class SearchView(BaseSearchView):
    template_name = "LZK/public/search.html"
