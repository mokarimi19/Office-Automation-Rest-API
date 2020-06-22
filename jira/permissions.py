from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from jira.models import CustomUser, Request, Department

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


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        print(CustomUser.objects.get(pk=view.kwargs["pk"]).department_name)
        print(request.user.department_name)

        # print(dir(view))
        # print(view.schema)

        return True

    # def has_object_permission(self, request, view, obj):
    # 	print("*" * 500)
    # 	print("has_object_permission !!!! {} - {} - {}".format(obj.myobj.id, obj.myobj.owner, request.user))
    # 	return True
    # return obj.myobj.owner == request.user



class UserIsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def check_object_permission(self, user, obj):
    	return False
        # return (user and user.is_authenticated() and
        #   (user.is_staff or obj == user))

    def has_object_permission(self, request, view, obj):
        return self.check_object_permission(request.user, obj)


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
    def  has_permission(self, request, view):
    	if request.method not in permissions.SAFE_METHODS and request.data:
    		return int(request.data['requester']) == request.user.pk
    	else:
	    	return True





class DashboardUpdatePermision(permissions.BasePermission):

	def has_permission(self, request, view):
		print("request.user.is_superuser", request.user.is_superuser)
		if request.user.is_superuser:
			return True
		emp_request = Request.objects.get(pk=view.kwargs['pk'])

		# if emp_request.requests_type[1] == "promotion" and not request.user.is_superuser:
		# 	return	False

		if not request.user.department_name:
			return False
		else:
			if not emp_request.requested_department.pk == request.user.department_name_id:
				return False
			else:
				if not request.user.pk in Department.objects.values_list("manager_id", flat=True):
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