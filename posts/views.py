from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.utils import inline_serializer
from rest_framework.generics import ListAPIView

from drf_spectacular.utils import extend_schema


from .selectors import get_hot_feed, get_recent_feed, get_top_feed, get_search_feed
from .serializers.post import (
    PostSerializer,
    PostCreateSerializer,
    post_detail_serialize,
    post_feed_serialize,
)
from .services import create_post, downvote_post, upvote_post, vote_poll, delete_post


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"


class AuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]


class FeedView(AuthMixin, ListAPIView, LimitOffsetPagination):
    def list(self, request):
        user = request.user

        post_ids = self.get_queryset()
        data = post_feed_serialize(
            post_ids=post_ids,
            fetched_by=user,
        )
        return self.get_paginated_response(data)


@extend_schema(responses=PostSerializer, operation_id="hot_list", tags=["feed"])
class HotFeedView(FeedView):
    def get_queryset(self):
        post_ids = get_hot_feed()
        return self.paginate_queryset(post_ids)


@extend_schema(responses=PostSerializer, operation_id="recent_list", tags=["feed"])
class RecentFeedView(FeedView):
    def get_queryset(self):
        post_ids = get_recent_feed()
        return self.paginate_queryset(post_ids)


@extend_schema(responses=PostSerializer, operation_id="top_list", tags=["feed"])
class TopFeedView(FeedView):
    def get_queryset(self):
        post_ids = get_top_feed()
        return self.paginate_queryset(post_ids, self.request, view=self)


class PostApi(AuthMixin, APIView):
    def get(self, request, post_id):
        user = request.user
        user = request.user
        return Response(post_detail_serialize(post_id=post_id, fetched_by=user))

    def delete(self, request, post_id):
        user = request.user
        delete_post(deleter=user, post_id=post_id)
        return Response({"success": True})


class CreatePostApi(AuthMixin, APIView):
    class CreatePostInputSerializer(serializers.Serializer):
        title = serializers.CharField()
        body = serializers.CharField(required=False, allow_blank=True)
        poll = inline_serializer(
            name="CreatePollInput",
            required=False,
            allow_null=True,
            fields={
                "options": serializers.ListField(child=serializers.CharField()),
            },
        )
        tagged_companies = inline_serializer(
            name="CreateTaggedCompanyInput",
            many=True,
            required=False,
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
        )

        class Meta:
            fields = ("title", "body", "poll", "tagged_companies")

    @extend_schema(
        request=CreatePostInputSerializer,
        responses=PostSerializer,
        operation_id="create_post",
        tags=["post"],
    )
    def post(self, request):
        user = request.user
        serializer = self.CreatePostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        post = create_post(creator=user, **data)
        response = post_detail_serialize(post_id=post.id, fetched_by=user)

        return Response(response)


class UpvotePostApi(AuthMixin, APIView):
    def put(self, request, post_id):
        user = request.user
        return upvote_post(user=user, post_id=post_id)


class DownvotePostApi(AuthMixin, APIView):
    def put(self, request, post_id):
        user = request.user
        return downvote_post(user=user, post_id=post_id)


class PollVoteApi(AuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        created_at = serializers.DateTimeField()
        ends_at = serializers.DateTimeField()
        total_votes = serializers.IntegerField(source="votes")
        user_selection = serializers.IntegerField()
        options = inline_serializer(
            many=True,
            fields={
                "id": serializers.IntegerField(),
                "body": serializers.CharField(),
                "vote_count": serializers.IntegerField(source="votes"),
            },
        )

    def post(self, request, poll_id, choice_id):
        user = request.user
        poll_vote = vote_poll(user=user, poll_id=poll_id, choice_id=choice_id)

        poll = poll_vote.poll
        poll.user_selection = choice_id
        poll.options = poll.pollchoice_set.all()

        return Response(self.OutputSerializer(poll).data)


class SearchPostApi(AuthMixin, APIView):
    def get(self, request):
        user = request.user
        query = request.GET.get("q")
        if query:
            post_ids = get_search_feed(query=query)
            response = post_feed_serialize(post_ids=post_ids, fetched_by=user)
            return Response(response)

        return Response([])
