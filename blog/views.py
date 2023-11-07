from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse

from django.template import loader
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.utils import timezone
from django.urls import reverse
from display.models import Club
import json
from django.core.serializers import serialize
from django.db.models.query import QuerySet
# Create your views here.


class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "latest_blog_entries"

    def get_queryset(self):
       return Post.objects.filter(pub_date__lte=timezone.now(), approved=True).order_by("-pub_date")[:10]



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


def combined_generator(queryset1, queryset2):
    for obj in queryset1:
        yield obj

    for obj in queryset2:
        yield obj



def serialize_objects(objs):
    # Convert queryset or model instances to JSON serializable format
    if isinstance(objs, QuerySet):
        return json.loads(serialize('json', objs))
    else:
        return json.loads(serialize('json', [objs]))[0]
    
def ApprovalView(request):
    unapproved_clubs = Club.objects.filter(approved = False)
    unapproved_posts = Post.objects.filter(approved = False)
    
    combined = list(combined_generator(unapproved_clubs, unapproved_posts))
    serialized_combined = [serialize_objects(obj) for obj in combined]
    template = loader.get_template("blog/approval.html")
    context = {
        "combined_objects": json.dumps(serialized_combined),
    }
    return HttpResponse(template.render(context, request))


