from django.contrib import admin
from api.catalog import models


@admin.register(models.Catalog)
class CatalogAdmin(admin.ModelAdmin):
    pass
