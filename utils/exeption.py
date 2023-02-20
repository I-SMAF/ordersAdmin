from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Есть ошибки в формировании запроса.'
    default_code = 'bad_request'


class BusinessLogicException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Что-то пошло не так, обратитесь в поддержку.'
    default_code = 'business_logic_error'
