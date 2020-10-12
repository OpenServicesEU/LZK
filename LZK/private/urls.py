from django.urls import include, path

from . import views

app_name = "private"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("import/", views.ImportView.as_view(), name="import"),
    path("feedback/", views.ListFeedbackView.as_view(), name="feedback-list"),
    path(
        "feedback/create/", views.CreateFeedbackView.as_view(), name="feedback-create"
    ),
    path(
        "feedback/detail/<int:pk>/",
        views.DetailFeedbackView.as_view(),
        name="feedback-detail",
    ),
    path(
        "feedback/detail/<int:pk>/close/",
        views.CloseFeedbackView.as_view(),
        name="feedback-close",
    ),
    path(
        "feedback/detail/<int:pk>/abilities/",
        views.AbilityCommentView.as_view(),
        name="feedback-detail-abilities",
    ),
    path(
        "feedback/detail/<int:pk>/symptoms/",
        views.SymptomCommentView.as_view(),
        name="feedback-detail-symptoms",
    ),
    path(
        "feedback/detail/<int:pk>/skills/",
        views.SkillCommentView.as_view(),
        name="feedback-detail-skills",
    ),
    path(
        "comment/ability/<int:pk>/<str:action>/",
        views.ChangeAbilityCommentView.as_view(),
        name="comment-ability-change",
    ),
    path(
        "comment/symptom/<int:pk>/<str:action>/",
        views.ChangeSymptomCommentView.as_view(),
        name="comment-symptom-change",
    ),
    path(
        "comment/skill/<int:pk>/<str:action>/",
        views.ChangeSkillCommentView.as_view(),
        name="comment-skill-change",
    ),
]
