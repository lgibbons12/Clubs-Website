from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Club
from django.views import generic
from django.utils import timezone
from django.urls import reverse


class IndexView(generic.ListView):
    template_name = "display/index.html"
    context_object_name = "club_list"
    
    

    def get_queryset(self):
        return Club.objects.order_by("name")

class DetailView(generic.DetailView):
    model = Club
    template_name = "display/detail.html"

    def get_queryset(self):
        return Club.objects

'''
class PostCreateView(generic.CreateView):
    model = Club
    fields = ["name", "pub_date", "words"]
    
    def get_success_url(self):
        return reverse("display:index")

    def form_valid(self, form):
        # Set the 'pub_date' field to the current date and time
        form.instance.pub_date = timezone.now()
        return super().form_valid(form)
        '''