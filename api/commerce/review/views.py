from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.clayful_client import ClayfulReviewClient
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def reviews_count(request, *args, **kwargs):
    clayful_review_client = ClayfulReviewClient()
    response = clayful_review_client.reviews_count(product=kwargs['product'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def reviews_list(request, *args, **kwargs):
    clayful_review_client = ClayfulReviewClient()
    response = clayful_review_client.reviews_count(product=kwargs['product'], page=kwargs['page'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_review(request, *args, **kwargs):
    clayful_review_client = ClayfulReviewClient()
    response = clayful_review_client.get_review(review_id=kwargs['review_id'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, *args, **kwargs):
    clayful_review_client = ClayfulReviewClient()
    response = clayful_review_client.create_review(
        customer=request.header['clayful'],
        order=request.data['order'],
        product=request.data['product'],
        rating=request.data['rating'],
        body=request.data['body'],
        images=request.data['images'],
        published=False
    )
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review(request, *args, **kwargs):
    clayful_review_client = ClayfulReviewClient()
    response = clayful_review_client.delete_review(
        customer=request.header['clayful'],
        review_id=request.data['review_id'],
    )
    return Response(response.data, status=status.HTTP_200_OK)
