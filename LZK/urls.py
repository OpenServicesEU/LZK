"""
LZK URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from . import forms, views

urlpatterns = [
    path(
        "login/", LoginView.as_view(form_class=forms.AuthenticationForm), name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    path("saml2/", include("djangosaml2.urls")),
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("abilities/", views.AbilityListView.as_view(), name="ability-list"),
    path(
        "abilities/<str:pk>/", views.AbilityDetailView.as_view(), name="ability-detail"
    ),
    path("symptoms/", views.SymptomListView.as_view(), name="symptom-list"),
    path(
        "symptoms/<str:pk>/", views.SymptomDetailView.as_view(), name="symptom-detail"
    ),
    path("skills/", views.CompetenceLevelView.as_view(), name="skill-list"),
    path("skills/<int:pk>/", views.SkillDetailView.as_view(), name="skill-detail"),
    path("activities/<int:pk>/", views.ActivityView.as_view(), name="activity-detail"),
    path("feedback/", views.FeedbackView.as_view(), name="feedback"),
    path(
        "feedback/subject/<str:pk>/abilities/",
        views.AbilityFeedbackView.as_view(),
        name="feedback-ability",
    ),
    path(
        "comment/ability/<int:pk>/",
        views.AbilityCommentView.as_view(),
        name="comment-ability",
    ),
    path(
        "feedback/subject/<str:pk>/symptoms/",
        views.SymptomFeedbackView.as_view(),
        name="feedback-symptom",
    ),
    path(
        "comment/symptom/<int:pk>/",
        views.SymptomCommentView.as_view(),
        name="comment-symptom",
    ),
    path(
        "feedback/activity/<int:pk>/skills/",
        views.SkillFeedbackView.as_view(),
        name="feedback-skill",
    ),
    path(
        "comment/skill/<int:pk>/",
        views.SkillCommentView.as_view(),
        name="comment-skill",
    ),
    path("secure/", include("LZK.private.urls", namespace="private")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
