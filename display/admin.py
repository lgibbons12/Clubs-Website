from django.contrib import admin, messages
from .models import Club
# Register your models here.
from google_sheets import sheets
from email_schedule import coolmain
from django.shortcuts import redirect
import random

funny_words = [
    "Bumblebee", "Wobble", "Gobbledygook", "Quizzical", "Wiggly", "Snicker",
    "Blubber", "Flabbergasted", "Lollygag", "Gobbledygook", "Noodle", "Quibble",
    "Snollygoster", "Kerfuffle", "Doozy", "Brouhaha", "Giggly", "Gobsmacked",
    "Whippersnapper", "Lollygag", "Quokka", "Snollygoster", "Wobble", "Dunderhead",
    "Quizzical", "Quibble", "Higgledy-piggledy", "Bamboozle", "Noodle", "Gobbledygook",
    "Hullabaloo", "Snicker", "Flibbertigibbet", "Malarkey", "Noodledoodle", "Wobble",
    "Quibble", "Bumfuzzle", "Giggly", "Flummox"
]

@admin.action(description="Duplicate Club")
def dupe_club(modeladmin, request, queryset):
    for _ in range(5):
        for obj in queryset:
                obj.pk = None  # Set primary key to None to create a new instance
                obj.name = random.choice(funny_words)
                obj.approved = False
                obj.save()




@admin.action(description="Reset Club Information from A Spreadsheet")
def reset_sheets(modeladmin, request, queryset):
    #create club backup
    backup_clubs = list(Club.objects.values())

    #trying the deletion
    try:
        link = queryset.first().sheet_link
        obs = Club.objects.all()
        obs.delete()
        sheets.main(sheet=link)
    except:
         Club.objects.bulk_create([Club(**club) for club in backup_clubs])
         messages.error(request, f'API request failed. Try rerunning with correct link')
         return redirect('admin:display_club_changelist')
    
    messages.success(request, 'Clubs reset successfully!')


    

@admin.action(description="Remove Club from Spreadsheet")
def remove_from_sheet(modeladmin, request, queryset):
    queryset.delete()
    #add in here functionality to remove from spreadsheet

@admin.action(description="Send email to me test")
def send_email_to_me(modeladmin, request, queryset):
    coolmain.send_email()



class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Club Information", {"fields": ["leaders", "emails", "description", "approved"],
                              "classes": ["collapse"]}),
        ("Change the Sheet Linked", {'fields': ["sheet_link"]}),                      

    ]
    list_display = ["name", "leaders", "emails", "description"]
    #list_filter = ["name"]
    search_fields = ["name"]
    actions = [reset_sheets, remove_from_sheet, send_email_to_me, dupe_club]
    

admin.site.register(Club, ClubAdmin)
