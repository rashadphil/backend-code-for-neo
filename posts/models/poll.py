from django.db import IntegrityError, models

from django.contrib.auth import get_user_model

User = get_user_model()


class Poll(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True)
    votes = models.IntegerField(default=0)

    class Meta:
        db_table = "poll"


class PollChoice(models.Model):
    body = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    class Meta:
        db_table = "poll_choice"
        ordering = ["id"]


class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll_choice = models.ForeignKey(PollChoice, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "poll_vote"

        indexes = [
            models.Index(fields=["user", "poll"]),
        ]
        unique_together = (("user", "poll"),)
