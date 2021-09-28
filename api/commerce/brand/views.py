from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulBrandClient
from .serializers import BrandRetrieveSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def get_brand(request, *args, **kwargs):
    clayful_brand_client = ClayfulBrandClient()
    try:
        response = clayful_brand_client.get_brand(brand_id=kwargs['brand_id'])
        if not response.status == 200:
            raise ValidationError({'error_msg': '상품을 불러올 수 없습니다.'})
        serializer = BrandRetrieveSerializer(response.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        raise ValidationError({'error_msg': '상품을 불러올 수 없습니다.'})
