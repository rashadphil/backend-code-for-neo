from typing import Iterable, List

from django.db.models import Prefetch
from rest_framework import serializers
from backend.users.models import User

from ..models.poll import PollVote
from ..models.post import Post
from ..models.tags import PostCompanyTag
from ..models.votes import PostVote
from ..services import user_can_delete_post
from .poll import PollReadSerializer
from .tags import CompanyTagSerializer

from django.db.models import Case, When


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    body = serializers.CharField(required=False, allow_blank=True)
    poll = PollReadSerializer()
    vote_count = serializers.ReadOnlyField(source="votes")
    user_vote = serializers.IntegerField()
    tagged_companies = CompanyTagSerializer(many=True)
    can_delete = serializers.BooleanField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "body",
            "created_at",
            "username",
            "poll",
            "vote_count",
            "user_vote",
            "tagged_companies",
            "can_delete",
        )


class TaggedCompanyCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        fields = ("id", "name")


class PollCreateSerializer(serializers.Serializer):
    options = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ("options",)


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField(required=False, allow_blank=True)
    poll = PollCreateSerializer(required=False, allow_null=True)
    tagged_companies = TaggedCompanyCreateSerializer(many=True, required=False)

    class Meta:
        fields = ("title", "body", "poll", "tagged_companies")


def post_prefetch(*, post_ids: List[int], fetched_by: User) -> Iterable[Post]:
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(post_ids)])

    post_vote_prefetch = Prefetch(
        "postvote_set",
        queryset=PostVote.objects.filter(user=fetched_by),
        to_attr="user_votes",
    )

    poll_vote_prefetch = Prefetch(
        "poll__pollvote_set",
        queryset=PollVote.objects.filter(user=fetched_by),
        to_attr="user_poll_selections",
    )

    company_tag_prefetch = Prefetch(
        "postcompanytag_set",
        queryset=PostCompanyTag.objects.select_related("company"),
        to_attr="company_tags",
    )

    return (
        Post.objects.select_related("user", "poll")
        .prefetch_related(
            "poll__pollchoice_set",
            company_tag_prefetch,
            post_vote_prefetch,
            poll_vote_prefetch,
        )
        .filter(id__in=post_ids)
        .order_by(preserved)
    )


def post_feed_serialize(*, post_ids: List[int], fetched_by: User):
    if not post_ids:
        return []
    objects = post_prefetch(post_ids=post_ids, fetched_by=fetched_by)

    for post in objects:
        user_vote = post.user_votes[0].inc if post.user_votes else 0
        post.user_vote = user_vote
        post.body = post.body[:100]

        companies = (tag.company for tag in post.company_tags)
        post.tagged_companies = companies
        post.can_delete = user_can_delete_post(post=post, deleter=fetched_by)

    return PostSerializer(objects, many=True).data


def post_detail_serialize(*, post_id: int, fetched_by: User):
    objects = post_prefetch(post_ids=[post_id], fetched_by=fetched_by)
    post = objects[0]
    post.user_vote = post.user_votes[0].inc if post.user_votes else 0

    companies = (tag.company for tag in post.company_tags)
    post.tagged_companies = companies
    post.can_delete = user_can_delete_post(post=post, deleter=fetched_by)

    return PostSerializer(post).data
