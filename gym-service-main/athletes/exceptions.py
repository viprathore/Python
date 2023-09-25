from rest_framework.exceptions import APIException


class InvalidDatesException(APIException):
    status_code = 400
