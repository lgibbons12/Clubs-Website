from django.contrib import admin
from .models import Post, ThingsToApprove
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Post Information", {"fields": ["pub_date", "picture", "words", "approved"],
                              "classes": ["collapse"]}),

    ]
    list_display = ["name", "pub_date", "picture", "words"]
    list_filter = ["pub_date"]
    search_fields = ["name"]

class ThingsToApproveAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Posts", {'fields': ['posts']}),
        ("Clubs", {'fields': ['clubs']}),
        
    ]
admin.site.register(Post, PostAdmin)
admin.site.register(ThingsToApprove, ThingsToApproveAdmin)
