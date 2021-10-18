from rest_framework.decorators import api_view, permission_classes
from api.clayful_client import ClayfulReviewCommentClient
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def get_comments(request, *args, **kwargs):
    clayful_comment_client = ClayfulReviewCommentClient()
    response = clayful_comment_client.get_comments(review_id=request.data['review_id'])
    return Response(response.data, status=status.HTTP_200_OK)
