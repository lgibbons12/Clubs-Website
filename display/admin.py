from django.contrib import admin
from .models import Club
# Register your models here.
class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Club Information", {"fields": ["leaders", "emails", "description"],
                              "classes": ["collapse"]}),

    ]
    list_display = ["name", "leaders", "emails", "description"]
    #list_filter = ["name"]
    search_fields = ["name"]

admin.site.register(Club, ClubAdmin)
