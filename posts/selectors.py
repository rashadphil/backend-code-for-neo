from typing import Iterable
from django.contrib.auth import get_user_model
from .models.post import Post
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

User = get_user_model()


def get_recent_feed() -> Iterable[int]:
    return Post.objects.all().order_by("-created_at").values_list("id", flat=True)


def get_hot_feed() -> Iterable[int]:
    return Post.objects.all().order_by("-hotness").values_list("id", flat=True)


def get_top_feed() -> Iterable[int]:
    return Post.objects.all().order_by("-votes").values_list("id", flat=True)


def get_search_feed(query: str) -> Iterable[int]:
    search_vector = SearchVector("title", "body", "postcompanytag__company__name")
    search_query = SearchQuery(query)
    return (
        Post.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
        )
        .filter(search=query)
        .values_list("id", flat=True)
        .order_by("-rank")
    )
