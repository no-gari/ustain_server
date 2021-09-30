from rest_framework.decorators import api_view
from .serializers import QNAListSerializer, QNACreateSerializer, \
    QNADeleteSerializer, QNACountSerializer, QNARetrieveSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
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
    try:
        clayful_review_client = ClayfulQNAClient()
        response = clayful_review_client.qna_list(product=kwargs['product'], page=kwargs['page'])
        if not response.status == 200:
            raise ValidationError({'error_msg': '서버 에러입니다. 다시 한 번 시도해주세요.'})
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '서버 에러입니다. 다시 한 번 시도해주세요.'})


@api_view(["GET"])
def get_qna(request, *args, **kwargs):
    try:
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        clayful_review_client = ClayfulQNAClient()
        response = clayful_review_client.get_qna(review_id=kwargs['review_id'])
        if not response.status == 200:
            raise ValidationError({'error_msg': '서버 에러입니다. 다시 한 번 시도해주세요.'})
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '서버 에러입니다. 다시 한 번 시도해주세요.'})


@api_view(["POST"])
def create_qna(request, *args, **kwargs):
    try:
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        clayful_review_client = ClayfulQNAClient()
        response = clayful_review_client.create_qna(
            customer=request.META['HTTP_CLAYFUL'],
            product=request.POST['product'],
            body=request.POST['body'],
            qnaReason=request.POST['qna_reason'],
        )
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '서버 에러입니다. 다시 한 번 시도해주세요.'})


@api_view(["DELETE"])
def delete_qna(request, *args, **kwargs):
    try:
        if not request.user.is_authenticated:
            return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
        clayful_review_client = ClayfulQNAClient()
        response = clayful_review_client.delete_qna(
            customer=request.header['clayful'],
            review_id=request.data['review_id'],
        )
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '서버 에러입니다. 다시 한 번 시도해주세요.'})
