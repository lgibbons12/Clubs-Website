from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse

from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Post, ThingsToApprove
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


    

def serialize_objects(objs):
    # Convert queryset or model instances to JSON serializable format
    if isinstance(objs, QuerySet):
        return json.loads(serialize('json', objs))
    else:
        return json.loads(serialize('json', [objs]))[0]
    
def ApprovalView(request):
    unapproved_posts = Post.objects.filter(approved=False)
    unapproved_clubs = Club.objects.filter(approved=False)

    # Create a ThingsToApprove instance without saving it to the database
    unapproved = ThingsToApprove()
    unapproved.save()

    # Use the set() method to associate posts and clubs with the unapproved instance
    unapproved.posts.set(unapproved_posts)
    unapproved.clubs.set(unapproved_clubs)

    num_posts = len(unapproved_posts)
    num_clubs = len(unapproved_clubs)
    context = {
        "posts_to_approve": num_posts,
        "clubs_to_approve": num_clubs,
        "mtm": unapproved
    }
    template = loader.get_template("blog/approval.html")
    
    return HttpResponse(template.render(context, request))


class ApprovalPostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/approve_post.html"

    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now())
    

class ApprovalClubDetailView(generic.DetailView):
    model = Club
    template_name = "blog/approve_club.html"

    def get_queryset(self):
        return Club.objects


def approval_code(request):
    
    if request.method == 'POST':
        # Retrieve the parameter from the POST data
        data = json.loads(request.body.decode('utf-8'))
        param = data.get('param', None)
        model = data.get("model", None)
        id = data.get("id", None)

        if param == "approved":
            if model == "post":
                item = get_object_or_404(Post, id=id)
                item.approved = True
                item.save()
        elif param == "denied":
            #deny the club
            print("denied")
            pass
        else:
            pass
        
        return redirect("blog:approval")
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Invalid request method'})