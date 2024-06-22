from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, default="", blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title