from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path("<int:user_id>/posts", views.UserPostsView.as_view(), name="user-posts"),
    path("me/posts", views.UserPostsView.as_view(), name="my-posts"),
    path("me/username", views.UpdateUsername.as_view(), name="update-username"),
    path("me", views.Me.as_view(), name="me"),
]
