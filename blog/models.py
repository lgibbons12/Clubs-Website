from django.db import models
from django.contrib import admin
from django.utils import timezone
import datetime
# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField()
    
    pub_date = models.DateTimeField("date published")
    words = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


