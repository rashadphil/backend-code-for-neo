from typing import Iterable
from django.contrib.auth import get_user_model
from posts.models.post import Post
from .models import Company
from posts.models.tags import PostCompanyTag

User = get_user_model()


def search_companies(*, query: str, limit: int = 10) -> Iterable[Company]:
    return Company.objects.filter(name__icontains=query).order_by("-score")[:limit]


def get_company_feed(
    *, company_id: int, order_by: str = "-created_at"
) -> Iterable[int]:
    post_ids = PostCompanyTag.objects.filter(company_id=company_id).values_list(
        "post_id", flat=True
    )

    return (
        Post.objects.filter(id__in=post_ids)
        .order_by(order_by)
        .values_list("id", flat=True)
    )
