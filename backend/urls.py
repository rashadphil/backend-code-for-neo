from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from backend.users.views import RegisterAPI, VerifyOTP
from rest_framework.schemas import get_schema_view
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework.settings import api_settings


router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/v1/", include(router.urls)),
    # path("register/", RegisterAPI.as_view()),
    # path("verify/", VerifyOTP.as_view()),
    path("api/v1/posts/", include("posts.urls")),
    # path("v1/companies/", include("companies.urls")),
    # path("api/v1/users/", include("backend.users.urls")),
    # path("api-token-auth/", views.obtain_auth_token),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    # Open API stuff
    path(
        "openapi",
        get_schema_view(
            title="Your Project",
            description="API for all things …",
            version="1.0.0",
            renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES,
        ),
        name="openapi-schema",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Redoc UI:
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
