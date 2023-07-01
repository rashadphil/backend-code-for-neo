from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("hot/", views.HotFeedView.as_view(), name="hot-posts"),
    path("recent/", views.RecentFeedView.as_view(), name="recent-posts"),
    path("top/", views.TopFeedView.as_view(), name="top-posts"),
    path("submit", views.CreatePostApi.as_view(), name="create-post"),
    # path("search/", views.SearchPostApi.as_view(), name="search-post"),
    # path("<int:post_id>/", views.PostApi.as_view(), name="delete-post"),
    # path("<int:post_id>/upvote/", views.UpvotePostApi.as_view(), name="upvote-post"),
    # path(
    #     "<int:post_id>/downvote/", views.DownvotePostApi.as_view(), name="downvote-post"
    # ),
    # path(
    #     "polls/<int:poll_id>/vote/<int:choice_id>",
    #     views.PollVoteApi.as_view(),
    #     name="poll-vote",
    # ),
]
