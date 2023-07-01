from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .emails import *
from .serializer import *

from .selectors import get_user_posts
from posts.serializers.post import post_feed_serialize

from .services import update_username

from rest_framework import status

User = get_user_model()


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"


class AuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]


class Me(AuthMixin, APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UpdateUsername(AuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()

    def post(self, request):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = update_username(user=user, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED, data=updated_user.username)


class UserPostsView(AuthMixin, APIView, LimitOffsetPagination):
    def get(self, request, user_id=None):
        fetched_by = request.user
        user_id = user_id or fetched_by.id  # get own posts if no user

        posts_by = get_object_or_404(User, pk=user_id)

        posts = get_user_posts(fetched_by=fetched_by, posts_by=posts_by)
        self.queryset = self.paginate_queryset(posts, request, view=self)

        data = post_feed_serialize(
            post_ids=posts, fetched_by=fetched_by, order_by="-votes"
        )

        return self.get_paginated_response(data)


class RegisterAPI(APIView):
    def post(self, request):
        print(request.data)
        try:
            data = request.data
            email = data.get("email")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(**data)

            if user.is_verified:
                return Response(
                    status=400,
                    data="User already exists",
                )
            else:
                send_otp_via_email(email)
                return Response(
                    status=200,
                    data="Registration Successful, check email for OTP",
                )

        except Exception as e:
            return Response(
                status=400,
                data="Registration Failed" + str(e),
            )


class VerifyOTP(APIView):
    def post(self, request):
        try:
            serializer = VerifyAccountSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.data["email"]
                otp = serializer.data["otp"]

                try:
                    user = User.objects.get(email=email)
                except:
                    return Response(
                        status=400,
                        data="Invalid email",
                    )

                if user.otp != otp:
                    return Response(
                        status=400,
                        data="Invalid OTP",
                    )

                user.is_verified = True
                user.save()

                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "user": {
                            "user_id": user.pk,
                            "email": user.email,
                        },
                        "token": token.key,
                    }
                )

        except Exception as e:
            return Response(
                {
                    "status": 400,
                    "message": "Something went wrong",
                    "data": str(e),
                }
            )
