from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView

from config.settings.base import SITE_NAME
from api.clayful_client import ClayfulCustomerClient
from api.commerce.product.serializers import ProductListByCategoriesSerializer


class ProductListByCategoriesView(CreateAPIView):
    serializer_class = ProductListByCategoriesSerializer