from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from jira.views import *

router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet, basename='Task')
router.register(r"users", CustomUserViewSet)
router.register(r"department", DepartmentViewSet)
router.register(r"request", RequestViewSet)
# router.register(r"dashboard", DashboardViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path("users/<int:pk>/fire", FireUserAPI.as_view()),
    path("dashboard/<int:pk>", DashboardUpdateViewset.as_view()),
    path("dashboard/", DashboardListViewset.as_view()),

    # path("users/<int:pk>/membership", MembershipRequestViewSet.as_view()),

    # url(r"users", UserCreate.as_view(), name="account-create"),
]
