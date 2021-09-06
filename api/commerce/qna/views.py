from rest_framework.decorators import api_view
from .serializers import QNAListSerializer, QNACreateSerializer, \
    QNADeleteSerializer, QNACountSerializer, QNARetrieveSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.clayful_client import ClayfulQNAClient
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def qna_count(request, *args, **kwargs):
    clayful_review_client = ClayfulQNAClient()
    response = clayful_review_client.qna_count(product=kwargs['product'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def qna_list(request, *args, **kwargs):
    clayful_review_client = ClayfulQNAClient()
    response = clayful_review_client.qna_list(product=kwargs['product'], page=kwargs['page'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_qna(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_review_client = ClayfulQNAClient()
    response = clayful_review_client.get_qna(review_id=kwargs['review_id'])
    return Response(response.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_qna(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_review_client = ClayfulQNAClient()
    response = clayful_review_client.create_qna(
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
def delete_qna(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    clayful_review_client = ClayfulQNAClient()
    response = clayful_review_client.delete_qna(
        customer=request.header['clayful'],
        review_id=request.data['review_id'],
    )
    return Response(response.data, status=status.HTTP_200_OK)
