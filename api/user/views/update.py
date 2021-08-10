from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer

from api.user.serializers.update import *
from api.user.models import User, EmailVerifier
from config.settings.base import SITE_NAME
