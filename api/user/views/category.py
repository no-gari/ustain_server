from api.user.serializers.category import CategorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from api.user.models import Categories


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    ordering = ['-id']
    queryset = Categories.objects.all()
