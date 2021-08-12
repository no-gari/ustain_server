from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
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
            email_verifier = EmailVerifier.objects.get(code=code, token=email_token)
        except EmailVerifier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='password_reset.html')
        # email 검증
        try:
            user = User.objects.get(email=email_verifier.email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='password_reset.html')

        return Response({'email_token': email_token, 'code': code, 'user': user, 'site_name': SITE_NAME},
                        template_name='password_reset.html')


class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer

    renderer_classes = [TemplateHTMLRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers, template_name='password_reset_complete.html')
