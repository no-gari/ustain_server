from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer

from api.user.serializers.base import *
from api.user.models import User, EmailVerifier
from config.settings.base import SITE_NAME


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer


class EmailFoundPhoneVerifierCreateView(CreateAPIView):
    serializer_class = EmailFoundPhoneVerifierCreateSerializer


class EmailFoundPhoneVerifierConfirmView(CreateAPIView):
    serializer_class = EmailFoundPhoneVerifierConfirmSerializer


class PasswordResetVerifyView(CreateAPIView):
    serializer_class = PasswordResetVerifySerializer


class PasswordResetView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        email_token = kwargs['email_token']
        code = kwargs['code']

        # email_token 검증
        try:
            email_verifier = EmailVerifier.objects.get(code=code, email_token=email_token)
        except EmailVerifier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # email 검증
        try:
            user = User.objects.get(email=email_verifier.email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({'email_token': email_token, 'user': user, 'site_name': SITE_NAME}, template_name='tmp.html')


class TmpView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        return Response({'site_name': SITE_NAME, 'num': kwargs['num']}, template_name='tmp.html')


class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer
