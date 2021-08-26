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
                    {'limit': 10,
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
            options = ({
                'customer': kwargs['customer'],
            })
            response = self.review.delete_for_me(review_id, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulQNAClient:
    def __init__(self):
        self.review = Clayful.Review

    def qna_count(self, **kwargs):
        try:
            options = {'query': {'product': kwargs['product'], 'published': True}}
            response = self.review.count(options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def qna_list(self, **kwargs):
        try:
            options = {
                'query':
                    {'limit': 10,
                     'product': kwargs['product'],
                     'page': kwargs['page'],
                     'sort': '-id',
                     'published': True
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

    def get_qna(self, **kwargs):
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

    def create_qna(self, **kwargs):
        try:
            payload = ({
                'order': kwargs['order'],
                'product': kwargs['product'],
                'rating': kwargs['rating'],
                'body': kwargs['body'],
                'images': kwargs['images'],
                'published': True,
                'meta': {
                    'qnaReason': kwargs['qnaReason']
                }
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

    def delete_qna(self, **kwargs):
        try:
            review_id = kwargs['review_id']
            options = ({
                'customer': kwargs['customer'],
            })
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

    def get_comment(self, **kwargs):
        try:
            review_id = kwargs['review_id']
            response = self.review_comment.get(review_id)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def create_comment(self, **kwargs):
        try:
            payload = {'review': kwargs['review_id'], 'body': kwargs['content']}
            options = {'customer': kwargs['clayful']}
            response = self.review_comment.create_for_me(payload, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def update_comment(self, **kwargs):
        try:
            payload = {'review': kwargs['review_id'], 'body': kwargs['content']}
            options = {'customer': kwargs['clayful']}
            response = self.review_comment.update_for_me(payload, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def delete_review(self, **kwargs):
        try:
            payload = {'review': kwargs['review_id'], 'body': kwargs['content']}
            options = {'customer': kwargs['clayful']}
            response = self.review_comment.delete_for_me(payload, options)
            return response
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


class ClayfulCartClient:
    def __init__(self):
        self.cart = Clayful.Cart

    def get_cart(self, **kwargs):
        try:
            payload = {}
            options = {
                'customer': kwargs['clayful'],
            }
            resposne = self.cart.get_for_me(payload, options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def add_to_cart(self, **kwargs):
        try:
            payload = {
                'product': kwargs['product'],
                'variant': kwargs['variant'],
                'quantity': kwargs['quantity'],
            }
            options = {'customer': kwargs['clayful']}
            resposne = self.cart.add_item_for_me(payload, options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def empty_all_cart(self, **kwargs):
        try:
            options = {'customer': kwargs['clayful']}
            resposne = self.cart.empty_for_me(options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def delete_item_cart(self, **kwargs):
        try:
            options = {'customer': kwargs['clayful']}
            resposne = self.cart.delete_item_for_me(kwargs['item_id'], options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def count_items_cart(self, **kwargs):
        try:
            options = {'customer': kwargs['clayful']}
            resposne = self.cart.count_items_for_me(options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})

    def checkout_cart(self, **kwargs):
        try:
            payload = {}
            options = {'customer': kwargs['clayful']}
            resposne = self.cart.checkout_for_me('order', payload, options)
            return resposne
        except Exception as err:
            error_msg = []
            if err.args:
                for error in err.args:
                    error_msg.append(error)
            return ValidationError({'error_msg': error_msg})


# class ClayfulCouponClient:
#     def __init__(self):
#         self.coupon = Clayful.Coupon
#
#
#
# class ClayfulOrderClient:
#     def __init__(self):
#         self.order = Clayful.Order
#
#
# class ClayfulPaymentClient:
#     def __init__(self):
#         self.payment = Clayful.Payment
