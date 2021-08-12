from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer

from api.user.serializers.login import *
from api.user.models import User, EmailVerifier
from config.settings.base import SITE_NAME


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer