from rest_framework import serializers
from api.catalog.models import Catalog


class CatalogListSerializers(serializers.ModelSerializer):
    model = Catalog


class CatalogRetrieveSerializer(serializers.ModelSerializer):
    model = Catalog
