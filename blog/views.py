from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.utils import timezone
# Create your views here.


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "latest_blog_entries"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]