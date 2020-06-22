from rest_framework.exceptions import APIException

class UserWithoutDepartmentException(APIException):
    status_code = 503
    default_detail = 'This Employee Belong to No Department.'