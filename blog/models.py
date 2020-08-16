from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=99)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='blogs')

