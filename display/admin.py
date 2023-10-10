from django.contrib import admin
from .models import Club
# Register your models here.
from google_sheets import sheets

def reset_sheets(modeladmin, request, queryset):
    if len(Club.objects.all()) > 3:
        return
    obs = Club.objects.all()
    obs.delete()
    sheets.main()

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
    actions = [reset_sheets]
    

admin.site.register(Club, ClubAdmin)
