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
            queryset = Task.objects.filter(
                assignee__in=dep_users
            )
        else:
            queryset = []
        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_superuser=False)
    serializer_class = CustomUserSerializer


class RequestViewSet(viewsets.ModelViewSet):
    # def get_object(self):
    #     print("salam" * 500)
    #     obj = get_object_or_404(Request.objects.filter(id=self.kwargs["pk"]))
    #     self.check_object_permissions(self.request, obj)
    #     print("get_object/ check_object_permissions")
    #     print(obj)
    #     return obj
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

    # def update(self, instance, validated_data):
    #     # Update the Foo instance
    #     print(validated_data)
    #     instance.save()
    #     return instance
    # def create(self, request, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     if  kwargs['pk'] == int(request.data['requester']):
    #         raise Exception("Guck")

    #     obj = self.get_object()
    #     print(obj)
    #     print(dir(obj))
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class ListUsers(APIView):

#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser, ]

#     def get(self, request, format=None):
#         request.get
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)

import rest_framework.generics
from rest_framework.views import APIView

# class FireUserAPI(APIView):
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         print(self.object)
#         print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
#         if self.object.department_name :
#             print("%" * 500)
#             print(department_name)
#             self.object.department_name = None
#         self.object.save()
#         serializer = self.get_serializer(self.object)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
#     print("Salam")
#     queryset = CustomUser.objects.all()
#     serializer_class = UpdateUserSerializer
#     print(queryset)

# class FireUserView(mixins.UpdateModelMixin):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = (permissions.IsAdminUser,)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         print(instance)
#         print(request.data.get("department_name"))
#         instance.save()

#         serializer = self.get_serializer(instance)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         return Response(serializer.data)


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


# class PromotionRequestViewSet(APIView):


# class MembershipRequestViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     queryset = Requests.objects.all()
#     serializer_class = RequestSerializer

# def create(self, request, pk=None):
#     queryset = CustomUser.objects.all()
#     user = get_object_or_404(queryset, pk=pk)
#     requester = request.user
#     print(request)
#     print(dir(request))
#     print(request.data)
#     req = Requests(requester=requester, requested_department="x", request_type="m")

#     serializer = RequestSerializer(req)
#     return Response(serializer.data)
