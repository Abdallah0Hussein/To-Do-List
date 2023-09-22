from django.db import models
from django.utils import timezone

# Create your models here.

class Task(models.Model):

    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, default=1)
    deadline = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    # Defines how an object should be represented as a string when it is converted to a string.
    def __str__(self):
        return f"Title: {self.title}"
