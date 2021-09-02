from api.user.serializers.email import EmailFoundPhoneVerifierCreateSerializer, EmailFoundPhoneVerifierConfirmSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.user.models import User


@api_view(["POST"])
@permission_classes([AllowAny])
def email_verifier(request, *args, **kwargs):
    email = request.data['email']
    try:
        User.objects.get(email=email)
    except:
        return Response(email, status=status.HTTP_200_OK)
    return Response({'error_msg': '이미 등록된 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)


class EmailFoundPhoneVerifierCreateView(CreateAPIView):
    serializer_class = EmailFoundPhoneVerifierCreateSerializer


class EmailFoundPhoneVerifierConfirmView(CreateAPIView):
    serializer_class = EmailFoundPhoneVerifierConfirmSerializer
