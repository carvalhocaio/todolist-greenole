from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.models import Group, User
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("todo.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

admin.site.site_header = "Greenole Admin"
admin.site.site_title = "Greenole Admin"
admin.site.index_title = "Welcome to Greenole Admin"
admin.site.unregister(Group)
admin.site.unregister(User)
