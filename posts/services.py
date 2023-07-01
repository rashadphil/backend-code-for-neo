import json
from typing import List

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models.poll import Poll, PollChoice, PollVote
from .models.post import Post
from .models.tags import PostCompanyTag
from companies.models import Company
from .models.votes import PostVote

User = get_user_model()


def populate_companies_table(*, file_path: str):
    with open(file_path) as f:
        data = json.load(f)

    companies = [
        Company(
            name=company_obj.get("name"),
            logo=company_obj.get("logo"),
            score=company_obj.get("score"),
            verified=True,
        )
        for company_obj in data
    ]

    Company.objects.bulk_create(companies)


def create_poll_choices(*, poll: Poll, options: List[str]) -> List[PollChoice]:
    poll_choices = [PollChoice(poll=poll, body=choice) for choice in options]
    PollChoice.objects.bulk_create(poll_choices)
    return poll_choices


def create_poll(*, options: List[str]) -> Poll:
    poll = Poll.objects.create()
    create_poll_choices(poll=poll, options=options)
    return poll


def create_tagged_companies(*, post: Post, companies: dict):
    tagged_companies = [
        PostCompanyTag(post=post, company_id=company.get("id")) for company in companies
    ]

    PostCompanyTag.objects.bulk_create(tagged_companies)


def create_post(
    *,
    creator: User,
    title: str,
    body: str = "",
    poll: dict = None,
    tagged_companies: dict = None,
) -> Post:
    poll = create_poll(options=poll.get("options")) if poll else None

    post = Post.objects.create(
        user=creator,
        title=title,
        body=body,
        poll=poll,
    )

    if tagged_companies:
        create_tagged_companies(post=post, companies=tagged_companies)

    return post


def user_can_delete_post(*, post: Post, deleter: User) -> bool:
    return post.user == deleter


def delete_post(*, post_id: int, deleter: User) -> None:
    post = get_object_or_404(Post, id=post_id)
    if not user_can_delete_post(post=post, deleter=deleter):
        return Response({"error": "You can only delete your own posts."}, status=403)
    post.delete()


def update_vote_count(*, prev_vote: int, post_vote: PostVote, post: Post) -> None:
    if prev_vote == 1:
        post.num_upvotes -= 1
    elif prev_vote == -1:
        post.num_downvotes -= 1

    if post_vote.inc == 1:
        post.num_upvotes += 1
    elif post_vote.inc == -1:
        post.num_downvotes += 1

    post.votes = post.num_upvotes - post.num_downvotes

    post.save()


def upvote_post(*, post_id: int, user: User) -> None:
    post = get_object_or_404(Post, id=post_id)
    vote, created = PostVote.objects.get_or_create(
        user=user, post=post, defaults={"inc": 0}
    )

    if vote.inc == 1:
        return retract_vote_post(post=post, vote=vote)
    else:
        prev_vote = vote.inc
        vote.inc = 1
        vote.save()
        update_vote_count(prev_vote=prev_vote, post_vote=vote, post=post)

    return Response({"success": True})


def downvote_post(*, post_id: int, user: User) -> None:
    post = get_object_or_404(Post, id=post_id)
    vote, created = PostVote.objects.get_or_create(
        user=user, post=post, defaults={"inc": 0}
    )

    if vote.inc == -1:
        return retract_vote_post(post=post, vote=vote)
    else:
        prev_vote = vote.inc
        vote.inc = -1
        vote.save()
        update_vote_count(prev_vote=prev_vote, post_vote=vote, post=post)

    return Response({"success": True})


def retract_vote_post(*, post: Post, vote: PostVote) -> None:
    prev_vote = vote.inc
    vote.inc = 0
    vote.save()
    update_vote_count(prev_vote=prev_vote, post_vote=vote, post=post)
    return Response({"success": True})


def increment_poll_vote_count(*, poll_vote: PollVote) -> None:
    poll = poll_vote.poll
    poll.votes += 1
    poll.save()

    poll_choice = poll_vote.poll_choice
    poll_choice.votes += 1
    poll_choice.save()


def vote_poll(*, poll_id: int, choice_id: int, user: User) -> PollVote:
    poll = get_object_or_404(Poll, id=poll_id)
    choice = get_object_or_404(PollChoice, id=choice_id)

    poll_vote, created = PollVote.objects.get_or_create(
        user=user, poll=poll, poll_choice=choice
    )

    if created:
        increment_poll_vote_count(poll_vote=poll_vote)

    return poll_vote
