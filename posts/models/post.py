from django.db import models

from django.contrib.auth import get_user_model

from django.apps import apps

from .poll import Poll

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)
    hotness = models.IntegerField(default=0)
    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)

    class Meta:
        db_table = "post"
        indexes = [models.Index(fields=["created_at", "votes", "hotness"])]
        ordering = ["-created_at", "-votes", "-hotness"]
