from rest_framework.exceptions import ValidationError
from django.conf import settings
from clayful import Clayful

Clayful.config({
            'language': 'ko',
            'currency': 'KRW',
            'time_zone': 'Asia/Seoul',
            'debug_language': 'ko',
            'client': settings.CLAYFUL_BACKEND_TOKEN
})


class ClayfulCustomerClient:
    def __init__(self):
        super().__init__()
        self.customer = Clayful.Customer

    def clayful_register(self, **kwargs):
        customer = self.customer
        payload = ({'connect': True, 'userId': kwargs['email']})
        try:
            response = customer.create(payload)
            return response
        except Exception as e:
            return ValidationError(e)

    def clayful_login(self, **kwargs):
        customer = self.customer
        payload = ({'userId': kwargs['email']})
        try:
            response = customer.authenticate(payload)
            return response
        except Exception as e:
            return ValidationError(e)

    def clayful_customer_delete(self, **kwargs):
        customer = self.customer
        options = ({'customer': kwargs['clayful']})
        try:
            response = customer.delete_me(options)
            return response
        except Exception as e:
            return ValidationError(e)


class ClayfulProductClient:
    def __init__(self):
        super().__init__()
        self.product = Clayful.Product

    def list_categories(self, **kwargs):
        try:
            options = {
                'query': {
                    'collection': kwargs['collection']
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'product_list': [err.message]})

    def get_detail(self, **kwargs):
        try:
            product_id = kwargs['id']
            response = self.product.get(product_id)
            return response
        except Exception as err:
            return ValidationError({'product_detail': [err.message]})


class ClayfulWishListClient:
    def __init__(self, auth_token):
        self.wishlist = Clayful.WishList
        self.options = {
            'customer': auth_token
        }
        self.wishlist_id = self.get_wishlist_id()

    def create_wishlist(self, **kwargs):
        try:
            payload = {
                'name': kwargs['name']
            }
            # options = {
            #     'customer': kwargs['customer_auth_token']
            # }
            response = self.wishlist.create_for_me(payload, self.options)
            return response
        except Exception as err:
            return ValidationError({'create_wishlist': [err.message]})

    def get_wishlist_id(self):
        try:
            response = self.wishlist.list_for_me(self.options)
            if len(response.data) == 0:
                self.create_wishlist(name='wishlist')
                return self.get_wishlist_id()
            return response.data[0]['_id']
        except Exception as err:
            raise ValidationError({'get_wishlist_id': [err.message]})

    def add_item(self, **kwargs):
        try:
            payload = {
                'product': kwargs['product_id']
            }
            response = self.wishlist.add_item_for_me(self.wishlist_id, payload, self.options)
            return response
        except Exception as err:
            raise ValidationError({'add_item': [err.message]})

    def delete_item(self, **kwargs):
        try:
            response = self.wishlist.delete_item_for_me(self.wishlist_id, kwargs['product_id'], self.options)
            return response
        except Exception as err:
            raise ValidationError({'delete_item': [err.message]})

    def empty_wishlist(self):
        try:
            response = self.wishlist.empty_for_me(self.wishlist_id, self.options)
            return response
        except Exception as err:
            raise ValidationError({'empty_wishlist': [err.message]})

    def get_list_products(self):
        try:
            response = self.wishlist.list_products_for_me(self.wishlist_id, self.options)
            return response
        except Exception as err:
            raise ValidationError({'get_list_products': [err.message]})


class ClayfulCartClient:
    def __init__(self, auth_token):
        self.cart = Clayful.Cart
        self.options = {
            'customer': auth_token
        }

    def get_cart(self):
        try:
            response = self.cart.get_for_me({},self.options)
            return response
        except Exception as err:
            raise ValidationError({'get_cart': [err.message]})

    def get_selected_items(self, **kwargs):
        try:
            self.options.update({
                'items': kwargs['items']
            })
            response = self.cart.get_for_me({},self.options)
            return response
        except Exception as err:
            raise ValidationError({'get_selected_items': [err.message]})

    def add_item(self, **kwargs):
        try:
            payload = {
                'product': kwargs['product_id'],
                'variant': kwargs['variant'],
                'quantity': kwargs['quantity']
            }
            response = self.cart.add_item_for_me(payload, self.options)
            print(response.data)
            return response
        except Exception as err:
            raise ValidationError({'add_item': [err.message]})

    def delete_item(self, **kwargs):
        try:
            response = self.cart.delete_item_for_me(kwargs['item_id'], self.options)
            return response
        except Exception as err:
            raise ValidationError({'delete_item': [err.message]})

    def empty_cart(self):
        try:
            response = self.cart.empty_for_me(self.options)
            return response
        except Exception as err:
            return ValidationError({'empty_cart': [err.message]})