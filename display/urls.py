from django.urls import path

from . import views
app_name = "display"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="club"),
    path("form/", views.ClubCreateView.as_view(), name="form")
]