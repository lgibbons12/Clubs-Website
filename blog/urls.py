from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("form/", views.PostCreateView.as_view(), name="form"),
    path("approval/", views.ApprovalView, name='approval')
]