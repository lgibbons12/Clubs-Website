from django.db import models

# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=50)
    #picture = models.ImageField()
    leaders = models.CharField(max_length=50)
    emails = models.EmailField()
    description = models.CharField(max_length=250)
