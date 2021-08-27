from rest_framework.exceptions import APIException


class ClayfulBrandException(APIException):
    status_code = 400
    default_detail = '브랜드 정보를 가져오는데 실패했습니다.'
