from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from .models import Club
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from google_sheets import return_linky
from .forms import ClubSearchForm
from django.http import JsonResponse

class IndexView(generic.ListView):
    template_name = "display/index.html"
    context_object_name = "club_list"
    
    def get_queryset(self):
        queryset = Club.objects.filter(approved=True)

        # Handle search query
        search_query = self.request.GET.get('search_query')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ClubSearchForm(self.request.GET)
        return context

class DetailView(generic.DetailView):
    model = Club
    template_name = "display/detail.html"

    def get_queryset(self):
        return Club.objects


class ClubCreateView(generic.CreateView):
    model = Club
    fields = ["name", "leaders", "emails", "description"]
    
    def form_valid(self, form):
        # Set the sheet_link attribute dynamically here
        # Assuming `get_dynamic_sheet_link` is a method from your package that provides the link
        form.instance.sheet_link = return_linky.grab()

        # Call the parent class's form_valid method to save the object
        response = super().form_valid(form)

        # Now you can perform any additional actions after the object is saved

        return response
    def get_success_url(self):
        return reverse("display:index")

    

def club_details(request):
    club_id = request.GET.get('club_id', None)
    if club_id:
        club = get_object_or_404(Club, id=club_id)
        return render(request, 'display/club_detail_partial.html', {'club': club})
    else:
        return JsonResponse({'error', 'Invalid request'})