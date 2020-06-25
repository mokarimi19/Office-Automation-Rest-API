import rest_framework.generics
from rest_framework.views import APIView
from rest_framework import viewsets
from jira.models import *
from jira.serializers import *
from jira.permissions import *
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsManagerOrOwnerOrAdminTask,
    ]

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "PUT":
            return UpdateTaskSerialier
        return TaskSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Task.objects.all()
        elif self.request.user.pk in Department.objects.values_list(
            "manager_id", flat=True
        ):
            dep_users = CustomUser.objects.filter(
                department_name=self.request.user.department_name
            )
            queryset = Task.objects.filter(assignee__in=dep_users)
        else:
            queryset = []
        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [
        CustomUserPermission,
    ]
    queryset = CustomUser.objects.filter(is_superuser=False)
    # serializer_class = CustomUserSerializer
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateUserSerializer
        return CustomUserSerializer


class RequestViewSet(viewsets.ModelViewSet):

    permission_classes = (IsOwneOfRequestOrAdmin,)
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class DashboardUpdateViewset(generics.RetrieveUpdateAPIView):

    permission_classes = (
        IsAuthenticated,
        DashboardUpdatePermision,
    )
    # queryset = self.get_queryset()
    queryset = Request.objects.filter(status__isnull=True)
    serializer_class = DashboardSerializer


class UserUpdateViewset(generics.RetrieveUpdateAPIView):

    permission_classes = (CustomUserPermission,)
    # queryset = self.get_queryset()
    queryset = CustomUser.objects.all()
    serializer_class = DashboardSerializer


class DashboardListViewset(generics.ListAPIView):
    # queryset = Request.objects.filter(status__isnull=True)
    serializer_class = DashboardSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Request.objects.filter(status__isnull=True)
        elif self.request.user.pk in Department.objects.values_list(
            "manager_id", flat=True
        ):
            queryset = Request.objects.filter(
                Q(status__isnull=True)
                & Q(requested_department=self.request.user.department_name)
            )
        else:
            queryset = []
        return queryset


class FireUserAPI(APIView):

    permission_classes = [
        IsAdminUser,
    ]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        if instance.department_name:
            print("%" * 500)
            instance.department_name = None
        instance.save()
        serializer = UpdateUserSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
