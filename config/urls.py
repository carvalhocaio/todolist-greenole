from django.urls import path
from django.contrib import admin
from django.contrib.auth.models import Group, User

urlpatterns = [
    path("admin/", admin.site.urls),
]

admin.site.site_header = "Greenole Admin"
admin.site.site_title = "Greenole Admin"
admin.site.index_title = "Welcome to Greenole Admin"
admin.site.unregister(Group)
admin.site.unregister(User)
