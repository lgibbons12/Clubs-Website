from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("form/", views.PostCreateView.as_view(), name="form"),
    path("approval/", views.ApprovalView, name='approval'),
    path("approval/post/<int:pk>/", views.ApprovalPostDetailView.as_view(), name="approval_post_detail"),
    path("approval/club/<int:pk>/", views.ApprovalClubDetailView.as_view(), name="approval_club_detail"),
    path("processing/", views.approval_code, name="approval_code"),
    path("next/", views.approve_next, name="approve_next")
]