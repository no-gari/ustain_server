from rest_framework.decorators import api_view, permission_classes
from api.clayful_client import ClayfulBrandClient
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def get_brand(request, *args, **kwargs):
    clayful_brand_client = ClayfulBrandClient()
    response = clayful_brand_client.get_brand(brand_id=kwargs['brand_id'])
    return Response(response.data, status=status.HTTP_200_OK)
