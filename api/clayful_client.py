from rest_framework.exceptions import ValidationError
from django.conf import settings
from clayful import Clayful


class ClayfulClient:
    def __init__(self):
        self.clf_key = settings.CLAYFUL_API_KEY
        self.clf_token = settings.CLAYFUL_BACKEND_TOKEN
        self.clf_secret = settings.CLAYFUL_API_SECRET

    Clayful.config({
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko'
    })


class ClayfulCustomerClient(ClayfulClient):
    def __init__(self):
        super().__init__()
        self.customer = Clayful.Customer

    def clayful_register(self, **kwargs):
        customer = self.customer
        payload = ({'connect': True, 'userId': kwargs['email']})
        options = ({'client': self.clf_token})
        try:
            response = customer.create(payload, options)
            return response
        except Exception as e:
            return ValidationError(e)

    def clayful_login(self, **kwargs):
        customer = self.customer
        payload = ({'userId': kwargs['email']})
        options = ({'client': self.clf_token})
        try:
            response = customer.authenticate(payload, options)
            return response
        except Exception as e:
            return ValidationError(e)

    def clayful_customer_delete(self, **kwargs):
        customer = self.customer
        options = ({'customer': kwargs['clayful'], 'client': self.clf_token})
        try:
            response = customer.delete_me(options)
            return response
        except Exception as e:
            return ValidationError(e)


class ClayfulProductClient(ClayfulClient):
    def __init__(self):
        super().__init__()
        self.product = Clayful.Product
