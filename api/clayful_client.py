from django.conf import settings
from clayful import Clayful


class ClayfulClient:
    def __init__(self):
        self.clf_key = settings.CLAYFUL_API_KEY
        self.clf_token = settings.CLAYFUL_BACKEND_TOKEN
        self.clf_secret = settings.CLAYFUL_API_SECRET
        self.customer = Clayful.Customer
        self.product = Clayful.Product

    Clayful.config({
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko'
    })

    # 회원가입, 로그인, 로그아웃, 회원 탈퇴
    def clayful_register(self, **kwargs):
        customer = self.customer
        payload = ({'userId': kwargs['id'], 'password': kwargs['password']})
        options = ({'client': self.clf_token})
        response = customer.create(payload, options)
        return response

    def clayful_login(self, **kwargs):
        customer = self.customer
        payload = ({'userId': kwargs['id'], 'password': kwargs['password']})
        options = ({'client': self.clf_token})
        response = customer.authenticate(payload, options)
        return response

    def clayful_logout(self, **kwargs):
        pass

    def clayful_customer_delete(self, **kwargs):
        pass

    # 상품 목록 / 상품 상세 가져오기