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
            return ValidationError({'error_msg': [e.args]})

    def clayful_login(self, **kwargs):
        customer = self.customer
        payload = ({'userId': kwargs['email']})
        try:
            response = customer.authenticate(payload)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})

    def clayful_customer_delete(self, **kwargs):
        customer = self.customer
        options = ({'customer': kwargs['clayful']})
        try:
            response = customer.delete_me(options)
            return response
        except Exception as e:
            return ValidationError({'error_msg': [e.args]})


class ClayfulProductClient:
    def __init__(self):
        super().__init__()
        self.product = Clayful.Product

    def get_related_products(self, **kwargs):
        try:
            options = {
                'query': {
                    'brand': kwargs['brand_id'],
                    'limit': 100,
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def list_products(self, **kwargs):
        try:
            options = {
                'query': {
                    'collection': kwargs.get('collection', 'any'),
                    'limit': 10,
                    'page': kwargs.get('page', 1),
                    'sort': kwargs.get('sort', '-createdAt'),
                    'brand': kwargs.get('brand', 'any')
                }
            }
            response = self.product.list(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def get_detail(self, **kwargs):
        try:
            product_id = kwargs['id']
            options = {'query': {'embed': '+brand.logo'}}
            response = self.product.get(product_id, options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def count_products(self, **kwargs):
        try:
            options = {'query': {'collection': kwargs.get('collection', 'any'), 'brand': kwargs.get('brand', 'any')}}
            response = self.product.count(options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})


class ClayfulBrandClient:
    def __init__(self):
        self.brand = Clayful.Brand

    def get_brand(self, **kwargs):
        try:
            brand_id = kwargs['brand_id']
            response = self.brand.get(brand_id)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulCollectionClient:
    def __init__(self):
        self.collection = Clayful.Collection

    def get_collections(self, **kwargs):
        try:
            parent = kwargs.get('parent', None)
            if parent is None:
                options = {'query': {'parent': 'none'}}
            else:
                options = {'query': {'parent': parent}}
            response = self.collection.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def get_collection(self, **kwargs):
        try:
            parent = kwargs.get('parent')
            response = self.collection.get(parent)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulReviewClient:
    def __init__(self):
        self.review = Clayful.Review

    def reviews_count(self, **kwargs):
        try:
            options = {'query': {'product': kwargs['product'], 'published': False}}
            response = self.review.count(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def reviews_list(self, **kwargs):
        try:
            options = {
                'query':
                    {
                        'limit': 10,
                        'product': kwargs['product'],
                        'page': kwargs['page'],
                        'sort': '-id',
                        'published': False
                    }
            }
            response = self.review.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def get_review(self, **kwargs):
        try:
            review_id = kwargs['review_id']
            options = {}
            response = self.review.get(review_id, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def create_review(self, **kwargs):
        try:
            payload = ({
                'order': kwargs['order'],
                'product': kwargs['product'],
                'rating': kwargs['rating'],
                'body': kwargs['body'],
                'images': kwargs['images'],
                'published': False
            })
            options = ({
                'customer': kwargs['customer'],
            })
            response = self.review.create_for_me(payload, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def delete_review(self, **kwargs):
        try:
            review_id = kwargs['review_id']
            options = {
                'customer': kwargs['customer'],
            }
            response = self.review.delete_for_me(review_id, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulReviewCommentClient:
    def __init__(self):
        self.review_comment = Clayful.ReviewComment

    def get_comments(self, **kwargs):
        try:
            options = {'query': {'review': kwargs['review_id'], 'page': 1}}
            response = self.review_comment.list(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulCartClient:
    def __init__(self, auth_token):
        self.cart = Clayful.Cart
        self.options = {'customer': auth_token}

    def get_cart(self):
        try:
            response = self.cart.get_for_me({}, self.options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def add_item(self, **kwargs):
        try:
            payload = {'product': kwargs['product_id'], 'variant': kwargs['variant'], 'quantity': kwargs['quantity']}
            response = self.cart.add_item_for_me(payload, self.options)
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

    def count_items_cart(self, **kwargs):
        try:
            resposne = self.cart.count_items_for_me(self.options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def checkout_cart(self, **kwargs):
        try:
            payload = {
                'items': kwargs['items'],
            }
            resposne = self.cart.checkout_for_me('order', payload, self.options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulWishListClient:
    def __init__(self, **kwargs):
        self.wishlist = Clayful.WishList
        self.options = {'customer': kwargs['clayful']}
        self.wishlist_id = self.get_wishlist_id()

    def create_wishlist(self, **kwargs):
        try:
            payload = {'name': kwargs['name']}
            response = self.wishlist.create_for_me(payload, self.options)
            return response
        except Exception as err:
            return ValidationError({'error_msg': [err.message]})

    def get_wishlist_id(self):
        try:
            response = self.wishlist.list_for_me(self.options)
            if len(response.data) == 0:
                self.create_wishlist(name='wishlist')
                return self.get_wishlist_id()
            return response.data[0]['_id']
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def add_item(self, **kwargs):
        try:
            payload = {'product': kwargs['product_id']}
            response = self.wishlist.add_item_for_me(self.wishlist_id, payload, self.options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def delete_item(self, **kwargs):
        try:
            response = self.wishlist.delete_item_for_me(self.wishlist_id, kwargs['product_id'], self.options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def empty_wishlist(self):
        try:
            response = self.wishlist.empty_for_me(self.wishlist_id, self.options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def get_list_products(self, **kwargs):
        try:
            options = {'customer': kwargs['clayful'], 'query': {'limit': 10, 'page': kwargs['page']}}
            response = self.wishlist.list_products_for_me(self.wishlist_id, options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})

    def count_wishlist(self):
        try:
            response = self.wishlist.count_products_for_me(self.wishlist_id, self.options)
            return response
        except Exception as err:
            raise ValidationError({'error_msg': [err.message]})
