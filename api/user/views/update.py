import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from config.settings.base import SITE_NAME
from api.clayful_client import ClayfulCustomerClient
from api.user.models import User, EmailVerifier
from api.user.serializers.update import UserProfileSerializer, PhoneUpdateVerifierCreateSerializer, \
    PhoneUpdateVerifierConfirmSerializer, PasswordResetVerifierCreateSerializer, PasswordResetSerializer, \
    PasswordResetConfirmSerializer


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put', 'get', 'delete']

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        clayful_customer_delete = ClayfulCustomerClient.clayful_customer_delete(clayful=kwargs['clayful'])
        if not clayful_customer_delete.status_code == 204 or clayful_customer_delete.status_code == 200:
            raise ValidationError({'error_msg': '다시 한 번 시도해주세요.'})
        return super().delete(self, request, *args)


class PhoneUpdateVerifierCreateView(CreateAPIView):
    serializer_class = PhoneUpdateVerifierCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PhoneUpdateVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneUpdateVerifierConfirmSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PasswordResetVerifyView(CreateAPIView):
    serializer_class = PasswordResetVerifierCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]


class PasswordResetView(RetrieveAPIView):
    serializer_class = PasswordResetSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        email_token = kwargs['email_token']
        code = kwargs['code']

        # email_token 검증
        try:
            email_verifier = EmailVerifier.objects.get(code=code, token=email_token)
        except EmailVerifier.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='http404.html')
        # link 유효시간 검증
        try:
            time_del = datetime.datetime.now() - email_verifier.created
            if time_del.seconds > 3600:
                email_verifier.delete()
                return Response(status=status.HTTP_404_NOT_FOUND, template_name='http404.html')
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='http404.html')
        # email 검증
        try:
            user = User.objects.get(email=email_verifier.email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='http404.html')

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
        if serializer.data.get('error') is None:
            return Response(status=status.HTTP_201_CREATED, headers=headers, template_name='password_reset_complete.html')
        elif serializer.data.get('error')[0] == 1:
            email_token = serializer.data.get('email_token')
            code = serializer.data.get('code')
            email_verifier = EmailVerifier.objects.get(code=code, token=email_token)
            user = User.objects.get(email=email_verifier.email)
            error = serializer.data.get('error')[1]
            return Response({'email_token': email_token, 'code': code, 'user': user, 'site_name': SITE_NAME, 'error': error},
                            template_name='password_reset.html')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='http404.html')

