from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from jira.models import CustomUser, Request, Department
from jira.exceptions import UserWithoutDepartmentException

# class IsAdminUserOrReadOnly(IsAdminUser):

# def has_permission(self, request, view):
#     is_admin = super(
#         IsAdminUserOrReadOnly,
#         self).has_permission(request, view)
#     # Python3: is_admin = super().has_permission(request, view)
#     return request.method in SAFE_METHODS or is_admin

# def has_object_permission(self, request, view, obj):
#     print("has_object_permission !!!! {} - {} - {}".format(obj.myobj.id, obj.myobj.owner, request.user))
#     # return obj.myobj.owner == request.user
#     return True

from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class IsAdminUserOrReadOnly(IsAdminUser):
	def has_permission(self, request, view):
		is_admin = super(IsAdminUserOrReadOnly, self).has_permission(request, view)
		# Python3: is_admin = super().has_permission(request, view)
		return request.method in SAFE_METHODS or is_admin


class IsManagerOrOwnerOrAdminTask(permissions.BasePermission):
	def has_permission(self, request, view):
		print("request.method", request.method)
		print("request.data", request.data)
		if request.method in SAFE_METHODS:
			return True
		if request.user.is_superuser:
			if request.method == "POST":
				return False
			else:
				return True

		if request.data:
			print("9 " * 90)
			assignee_pk = request.data["assignee"].split("/")[-2]
			assignee = CustomUser.objects.get(pk=assignee_pk)
			print("assignee", assignee)
			if assignee_pk == request.user.pk:
				return True
			elif not assignee.department_name:
				raise UserWithoutDepartmentException
			elif (
				assignee.department_name.pk == request.user.department_name.pk
				and request.user.department_name.pk
				in Department.objects.values_list("manager_id", flat=True)
			):
				return True
		else:
			return True

	# def has_object_permission(self, request, view, obj):
	# 	print("*" * 500)
	# 	print("has_object_permission !!!! {} - {} - {}".format(obj.myobj.id, obj.myobj.owner, request.user))
	# 	return True
	# return obj.myobj.owner == request.user


# class UserIsOwnerOrAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated()

#     def check_object_permission(self, user, obj):
#     	return False
#         # return (user and user.is_authenticated() and
#         #   (user.is_staff or obj == user))

#     def has_object_permission(self, request, view, obj):
#         return self.check_object_permission(request.user, obj)


class CustomUserPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		if request.user.is_superuser:
			return True
		if 'pk' in view.kwargs:
			if not request.user.is_authenticated:
				return False
			if request.user.is_superuser and request.user.pk == CustomUser.objects.get(pk=view.kwargs["pk"]):
				return True
		else:
			return True

		# if request.method == "POST":
		# 	if not request.user.is_authenticated:
		# 		return True
	# def has_object_permission(self, request, view, obj):
	# 	print(view.kwargs["pk"])
	# 	if view.kwargs["pk"] == 
	# 	print("has_object_permission !!!! {} - {} - {}".format(obj.myobj.id, obj.myobj.owner, request.user))
	# 	# return obj.myobj.owner == request.user
	# 	return True

class IsOwneOfRequestOrAdmin(permissions.BasePermission):
	#### can write custom code
	# def has_permission(self, request, view):
	# 	# print(view.kwargs.get("id"))
	# 	# print(dir(view))
	# 	# print("*" * 50)
	# 	print(request.method, view)
	# 	if request.method == "POST":
	# 		print(view.kwargs)
	# 		# user = Request.objects.get(pk=view.kwargs["requester"])
	# 	return True
	def has_permission(self, request, view):
		if request.method not in permissions.SAFE_METHODS and request.data:
			return int(request.data["requester"]) == request.user.pk
		else:
			return True


class DashboardUpdatePermision(permissions.BasePermission):
	def has_permission(self, request, view):
		print("request.user.is_superuser", request.user.is_superuser)
		if request.user.is_superuser:
			return True
		emp_request = Request.objects.get(pk=view.kwargs["pk"])

		# if emp_request.requests_type[1] == "promotion" and not request.user.is_superuser:
		# 	return	False

		if not request.user.department_name:
			return False
		else:
			if (
				not emp_request.requested_department.pk
				== request.user.department_name_id
			):
				return False
			else:
				if not request.user.pk in Department.objects.values_list(
					"manager_id", flat=True
				):
					return False

		if request.method in permissions.SAFE_METHODS:
			return True

		# print("department_name", request.user.department_name.pk)
		# if request.data :
		# 	print("yes")
		# 	return True
		# print("dep " * 50)
		# print(request.data)
		# print(request.data['requested_department'])
		# if not request.user in managers or not request.user.is_superuser:
		# 	return False
		# if request.method not in permissions.SAFE_METHODS and request.data:

		# else:
		# 	return True
		# def has_object_permission(self, request, view, obj):
		#  print("salam")
		#  # if request.method in permissions.SAFE_METHODS:
		#  # 	return True
		#  # print(request.user.pk, obj.requester.pk)
		#  # print(request.user.pk == obj.requester.pk)
		#  # return request.user.pk == obj.requester.pk
		#  return False

		# return request.user.pk == obj.requester.pk
		# print(Request.objects.get(pk=view.kwargs['pk']))
		# if request.method == "POST":
		# 	print("salam")
		# 	print(request.user)
		# 	print(obj.requester)
