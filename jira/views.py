from rest_framework import viewsets
from jira.models import *
from jira.serializers import *
from permissions import  *
class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
	permission_classes = (IsAdminUserOrReadOnly,)
	queryset = Department.objects.all()
	serializer_class = DepartmentSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
		