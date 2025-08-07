from rest_framework.exceptions import APIException


class ObjectNotFound(APIException):
    status_code = 404
    default_detail = "Object not found."
    default_code = "object_not_found"