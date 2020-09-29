from django.urls import include, path

from . import views


app_name = "private"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("import/", views.ImportView.as_view(), name="import"),
    path("feedback/", views.ListFeedbackView.as_view(), name="feedback-list"),
    path("feedback/create/", views.CreateFeedbackView.as_view(), name="feedback-create"),
    path("feedback/detail/<int:pk>/", views.DetailFeedbackView.as_view(), name="feedback-detail"),
]
