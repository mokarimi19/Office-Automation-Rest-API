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
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    title = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)


class Department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    manager = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
