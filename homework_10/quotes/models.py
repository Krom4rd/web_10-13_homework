from typing import Any
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=70, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    born_date = models.DateTimeField()
    born_location = models.CharField(max_length=255)
    description = models.CharField(max_length = 2704)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','full_name', 'born_date', 'born_location', 'description'], name='author of username')
        ]

    def __str__(self) -> str:
        return self.full_name
    

class Quote(models.Model):
    description = models.CharField(null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    author = models.ManyToManyField(Author)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.author}"