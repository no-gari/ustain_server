from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.clayful_client import ClayfulCartClient
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.get_cart(clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.add_to_cart(
        product=request.data['product'],
        variant=request.data['variant'],
        quantity=request.data['quantity'],
        clayful=request.headers['clayful']
    )
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def empty_cart(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.empty_all_cart(clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_item(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.delete_item_cart(item_id=request.data['item_id'], clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def count_items(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.count_items_cart(clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)
