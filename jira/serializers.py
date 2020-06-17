from jira.models import *
from rest_framework import serializers
from jira.models import *


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ["assignee", "description", "title", "deadline"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["password", "username", "first_name", "last_name", "email"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = CustomUser(**validated_data)
        instance.set_password(password)
        instance.save()  # before saving you can do any data manipulation
        return instance
