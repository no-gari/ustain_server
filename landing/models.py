from datetime import timedelta, datetime
from django.db import models


class Order(models.Model):
    gift_name = models.CharField(max_length=512, verbose_name='상품 이름', null=True, blank=True, help_text='상품 이름입니다.')
    gift_url = models.URLField(verbose_name='상품 설명 url', null=False, blank=False)
    orderer_name = models.CharField(max_length=64, verbose_name='주문자 이름', null=True, blank=True, help_text='주문자 이름입니다.')
    orderer_phone = models.CharField(max_length=32, verbose_name='주문자 휴대폰 번호', null=True, blank=True, help_text='주문자 휴대폰 번호입니다.')
    gift_reason = models.TextField(verbose_name='선물 사유', null=True, blank=True, help_text='선물 사유가 들어갈 곳입니다.')
    message = models.TextField(verbose_name='전달하고싶은 메세지', null=True, blank=True, help_text='전달 메세지가 들어갈 곳입니다.')
    letter = models.TextField(verbose_name='종합 편지', null=True, blank=True, help_text='위 내용을 종합하셔서 편지로 만들어주세요.')
    letter_deliver = models.BooleanField(verbose_name='선물 전달 여부', default=False, help_text='편지 전달 완료 시 True로 바뀝닏나.')
    order_date = models.DateTimeField(verbose_name='주문 날짜', help_text='주문 날짜입니다.', default=datetime.now())
    reciever_name = models.CharField(max_length=64, verbose_name='선물 수령인', null=True, blank=True, help_text='선물 수령인입니다.')
    reciever_phone = models.CharField(max_length=64, verbose_name='선물 수령인 휴대폰 번호', null=True, blank=True, help_text='선물 수령인 휴대폰 번호입니다.')
    recieve_date = models.DateTimeField(verbose_name='배송지 입력 기간', default=datetime.now()+timedelta(days=7))
    reciever_big_address = models.TextField(verbose_name='수령인 주소', null=True, blank=True, help_text='선물 수령인 배송지입니다.')
    reciever_small_address = models.TextField(verbose_name='수령인 상세 주소', null=True, blank=True, help_text='선물 수령인 상세 배송지입니다.')
    reciever_requirements = models.TextField(verbose_name='수령인 요청사항', null=True, blank=True, help_text='선물 수령인 요청사항 입니다.')