from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Club
from django.views import generic
from google_sheets import sheets

class IndexView(generic.ListView):
    template_name = "display/index.html"
    context_object_name = "club_list"
    clubs_to_delete = Club.objects.all()
    clubs_to_delete.delete()
    sheets.main()

    def get_queryset(self):
        return Club.objects.order_by("name")

class DetailView(generic.DetailView):
    model = Club
    template_name = "display/detail.html"

    def get_queryset(self):
        return Club.objects
