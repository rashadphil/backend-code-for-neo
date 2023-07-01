import random

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from backend.users.models import User


def update_username(*, user: User, username: str) -> User:
    if len(username) < 3:
        raise ValueError("Username is too short")
    try:
        User.objects.get(username=username)
        raise ValueError("Username already exists")
    except User.DoesNotExist:
        user.username = username
        user.save()
        return user
