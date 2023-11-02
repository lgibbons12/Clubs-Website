from django import forms

class ClubSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Clubs', max_length=100)