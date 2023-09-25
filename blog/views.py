from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.utils import timezone
from django.urls import reverse
# Create your views here.


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "latest_blog_entries"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]


class PostView(generic.DetailView):
    model = Post
    template_name = "blog/post.html"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now())

class PostCreateView(generic.CreateView):
    model = Post
    fields = ["name", "pub_date", "words"]
    
    def get_success_url(self):
        return reverse("blog:index")

    def form_valid(self, form):
        # Set the 'pub_date' field to the current date and time
        form.instance.pub_date = timezone.now()
        return super().form_valid(form)