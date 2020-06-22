from jira.models import *
from rest_framework import serializers
from jira.models import *
from datetime import datetime
import pytz


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ["assignee", "description", "title", "deadline"]

    # def validate(self, values):
    #     print("*"*500)
    #     now = pytz.UTC.localize(datetime.now())
    #     deadline = pytz.UTC.localize(values['deadline'])
    #     print(now<deadline)
    #     print(now> datetime)
    #     return values


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ["password", "username", "first_name", "last_name", "email"]
        fields = "__all__"
        write_only_fields = ["password"]
        read_only_fields = [
            "groups",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "user_permissions",
            "department_name",
            "groups",
            "last_login",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = CustomUser(**validated_data)
        instance.set_password(password)
        instance.save()  # before saving you can do any data manipulation
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "department_name",
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        read_only_fields = [
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        # fields = "__all__"

    # def create(self, validated_data):
    #     password = validated_data.pop("password")
    #     instance = CustomUser(**validated_data)
    #     instance.set_password(password)
    #     instance.save()  # before saving you can do any data manipulation
    #     return instance


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        read_only_fields = ["status"]
    def validate_requested_department(self, value):
        print("request" * 50)
        if value.manager:
            raise serializers.ValidationError("This Department Already has Manager!!")
        return value


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            "id",
            "request_type",
            "requested_department",
            "requester",
            "status",
        )
        read_only_fields = (
            "id",
            "request_type",
            "requested_department",
            "requester",
        )

        write_only_fields = ("status",)

    def update(self, instance, validated_data):
        print("validated_data", validated_data)
        print("instance", instance)
        print("instance.request_type", instance.request_type)
        if validated_data:
            if validated_data["status"] == "a":
                if instance.request_type == "m":
                    user = instance.requester
                    user.department_name = instance.requested_department
                    user.save()
                elif instance.request_type == "e2m":
                    department = instance.requested_department
                    department.manager = instance.requester
                    department.save()
            if validated_data["status"] == "r":
                instance.delete()
        return instance
