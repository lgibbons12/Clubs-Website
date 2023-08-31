from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        ("Post Information", {"fields": ["pub_date"],
                              "classes": ["collapse"]}),
    ]
    list_display = ["name", "pub_date", "picture", "words"]
    list_filter = ["pub_date"]
    search_fields = ["name"]

admin.site.register(Post, PostAdmin)
