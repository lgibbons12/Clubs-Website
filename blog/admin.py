from django.contrib import admin
from .models import Post, ThingsToApprove
import random
# Register your models here.

funny_words = [
    "Bumblebee", "Wobble", "Gobbledygook", "Quizzical", "Wiggly", "Snicker",
    "Blubber", "Flabbergasted", "Lollygag", "Gobbledygook", "Noodle", "Quibble",
    "Snollygoster", "Kerfuffle", "Doozy", "Brouhaha", "Giggly", "Gobsmacked",
    "Whippersnapper", "Lollygag", "Quokka", "Snollygoster", "Wobble", "Dunderhead",
    "Quizzical", "Quibble", "Higgledy-piggledy", "Bamboozle", "Noodle", "Gobbledygook",
    "Hullabaloo", "Snicker", "Flibbertigibbet", "Malarkey", "Noodledoodle", "Wobble",
    "Quibble", "Bumfuzzle", "Giggly", "Flummox"
]

@admin.action(description="Duplicate Blog")
def dupe_blog(modeladmin, request, queryset):
    for _ in range(5):
        for obj in queryset:
                obj.pk = None  # Set primary key to None to create a new instance
                obj.name = random.choice(funny_words)
                obj.approved = False
                obj.save()

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Post Information", {"fields": ["pub_date", "picture", "words", "approved"],
                              "classes": ["collapse"]}),

    ]
    list_display = ["name", "pub_date", "picture", "words"]
    list_filter = ["pub_date"]
    search_fields = ["name"]
    actions = [dupe_blog]

class ThingsToApproveAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Posts", {'fields': ['posts']}),
        ("Clubs", {'fields': ['clubs']}),
        
    ]
admin.site.register(Post, PostAdmin)
admin.site.register(ThingsToApprove, ThingsToApproveAdmin)
