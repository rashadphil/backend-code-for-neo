from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path(
        "<int:company_id>/posts/hot",
        views.CompanyHotFeedView.as_view(),
        name="company-hot",
    ),
    path(
        "<int:company_id>/posts/recent",
        views.CompanyRecentFeedView.as_view(),
        name="company-recent",
    ),
    path("<int:company_id>", views.CompanyDetailView.as_view(), name="company-detail"),
    path("search", views.CompanySearchApi.as_view(), name="company-search"),
]
