from django.shortcuts import get_object_or_404
from posts.serializers.post import post_feed_serialize
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import get_company_feed, search_companies
from .models import Company


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"


class AuthMixin:
    authentication_classes = [BearerAuthentication]
    permission_classes = [IsAuthenticated]


class CompanyDetailView(AuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        logo = serializers.CharField()

    def get(self, request, company_id):
        company = get_object_or_404(Company, id=company_id)
        return Response(self.OutputSerializer(company).data)


class CompanyFeedView(AuthMixin, APIView, LimitOffsetPagination):
    def get(self, request, company_id):
        user = request.user
        self.company_id = company_id

        post_ids = self.get_queryset()
        data = post_feed_serialize(
            post_ids=post_ids,
            fetched_by=user,
        )
        return self.get_paginated_response(data)


class CompanyHotFeedView(CompanyFeedView):
    order_by = "-hotness"

    def get_queryset(self):
        post_ids = get_company_feed(company_id=self.company_id, order_by=self.order_by)
        return self.paginate_queryset(post_ids, self.request, view=self)


class CompanyRecentFeedView(CompanyFeedView):
    def get_queryset(self):
        post_ids = get_company_feed(company_id=self.company_id, order_by=self.order_by)
        return self.paginate_queryset(post_ids, self.request, view=self)


class CompanySearchApi(AuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        logo = serializers.CharField()

    def get(self, request):
        q = request.GET.get("q")
        LIMIT = 10
        companies = search_companies(query=q, limit=LIMIT)
        return Response(self.OutputSerializer(companies, many=True).data)
