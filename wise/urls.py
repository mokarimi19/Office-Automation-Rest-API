from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from jira.views import *

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"users", CustomUserViewSet)
router.register(r"department", DepartmentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    # url(r"users", UserCreate.as_view(), name="account-create"),
]
