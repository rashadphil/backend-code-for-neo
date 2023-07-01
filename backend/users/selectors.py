from typing import Iterable
from django.contrib.auth import get_user_model
from posts.models.post import Post

User = get_user_model()


def get_user_posts(*, fetched_by: User, posts_by: User) -> Iterable[int]:
    if fetched_by.id != posts_by.id:
        return []

    return Post.objects.filter(user_id=posts_by.id).values_list("id", flat=True)
