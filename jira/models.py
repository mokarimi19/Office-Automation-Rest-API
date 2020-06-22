from django.db import models
from django.contrib.auth.models import AbstractUser
from jira.managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("First Name", max_length=255, blank=True, null=False)
    last_name = models.CharField("Last Name", max_length=255, blank=True, null=False)
    department_name = models.ForeignKey(
        "Department", null=True, on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True,)
    is_staff = models.BooleanField(default=True)

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name"
    ]
    objects = CustomUserManager()

    class Meta:
        unique_together = (
            "first_name",
            "last_name",
        )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    assignee = models.ManyToManyField(CustomUser)
    description = models.TextField()
    title = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    # assigner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="task_assigner")


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    manager = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Request(models.Model):
    requests_type = [("m", "membership"), ("e2m", "promotion")]
    status_type = [("a", "accepted"), ("r", "rejected")]
    request_type = models.CharField(choices=requests_type, max_length=5)
    requested_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(choices=status_type, max_length=2, null=True)

