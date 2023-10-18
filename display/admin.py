from django.contrib import admin
from .models import Club
# Register your models here.
from google_sheets import sheets

@admin.action(description="Reset Club Information from Spreadsheet")
def reset_sheets(modeladmin, request, queryset):
    
    obs = Club.objects.all()
    obs.delete()
    sheets.main()

@admin.action(description="New Spreadsheet")
def new_sheet(modeladmin, request, queryset):
    link = queryset.first().sheet_link
    obs = Club.objects.all()
    obs.delete()
    sheets.main(sheet = link)
    

@admin.action(description="Remove Club from Spreadsheet")
def remove_from_sheet(modeladmin, request, queryset):
    queryset.delete()
    #add in here functionality to remove from spreadsheet

class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Club Information", {"fields": ["leaders", "emails", "description"],
                              "classes": ["collapse"]}),
        ("Change the Sheet Linked", {'fields': ["sheet_link"]}),                      

    ]
    list_display = ["name", "leaders", "emails", "description"]
    #list_filter = ["name"]
    search_fields = ["name"]
    actions = [reset_sheets, remove_from_sheet, new_sheet]
    

admin.site.register(Club, ClubAdmin)
