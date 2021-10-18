from api.catalog.views import CatalogsListView, CatalogRetrieveView
from django.urls import path

urlpatterns = [
    path('list/<str:distribute>', CatalogsListView.as_view()),
    path('<int:id>', CatalogRetrieveView.as_view()),
]
