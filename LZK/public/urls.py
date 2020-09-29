from django.urls import include, path

from . import views

app_name = "public"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("objectives/", views.ObjectiveSubjectListView.as_view(), name="objective-subject"),
    path("objectives/<str:pk>/", views.ObjectiveSubjectDetailView.as_view(), name="objective-subject-detail"),
    path("symptoms/", views.SymptomSubjectListView.as_view(), name="symptom-subject"),
    path("symptoms/<str:pk>/", views.SymptomSubjectDetailView.as_view(), name="symptom-subject-detail"),
    path("competence_levels/", views.CompetenceLevelView.as_view(), name="competence_level"),
    path("activity/<int:pk>/", views.ActivityView.as_view(), name="activity"),
    path("comment/", views.CommentView.as_view(), name="comment"),
    path(
        "comment/<int:pk>/",
        views.ObjectiveCommentView.as_view(),
        name="comment-objective",
    ),
]
