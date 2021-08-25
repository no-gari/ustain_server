from django.views.decorators.http import require_http_methods
from api.clayful_client import ClayfulBrandClient
from django.http import JsonResponse


@require_http_methods(["GET"])
def get_brand(request, *args, **kwargs):
    clayful_brand_client = ClayfulBrandClient()
    response = clayful_brand_client.get_brand(brand_id=kwargs['brand_id'])
    return JsonResponse({'response': response.data})
