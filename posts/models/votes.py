from django.db import IntegrityError, models
from django.contrib.auth import get_user_model

User = get_user_model()

from .post import Post


class PostVote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    inc = models.SmallIntegerField()

    class Meta:
        db_table = "post_vote"
        unique_together = (("post", "user"),)
        indexes = [
            models.Index(fields=["post", "user"]),
        ]

    @classmethod
    def upvote(cls, user, post):
        vote, created = PostVote.objects.get_or_create(
            user=user, post=post, defaults={"inc": 1}
        )

        if created:
            post.increment_vote_count()
        else:
            if vote.inc == 1:
                vote.inc = 0
                post.decrement_vote_count()
            elif vote.inc == -1:
                vote.inc = 1
                post.increment_vote_count(amount=2)
            else:
                vote.inc = 1
                post.increment_vote_count()

            vote.save()

        return vote, created

    @classmethod
    def downvote(cls, user, post):
        vote, created = PostVote.objects.get_or_create(
            user=user, post=post, defaults={"inc": -1}
        )

        if created:
            post.decrement_vote_count()
        else:
            if vote.inc == -1:
                vote.inc = 0
                post.increment_vote_count()
            elif vote.inc == 1:
                vote.inc = -1
                post.decrement_vote_count(amount=2)
            else:
                vote.inc = -1
                post.decrement_vote_count()

            vote.save()

        return vote, created
