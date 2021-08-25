from django.views.decorators.http import require_http_methods
from api.clayful_client import ClayfulCartClient
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_cart(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.get_cart(clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["POST"])
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
def empty_cart(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.empty_all_cart(clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_item(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.delete_item_cart(item_id=request.data['item_id'], clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def count_items(request, *args, **kwargs):
    clayful_cart_client = ClayfulCartClient()
    response = clayful_cart_client.count_items_cart(clayful=request.headers['clayful'])
    return Response(response.data, status=status.HTTP_200_OK)
