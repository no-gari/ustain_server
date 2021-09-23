from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from api.logger.models import PhoneLog
from .models import Order
import datetime
import hashlib


class RecieverView(DetailView):
    model = Order
    template_name = 'main.html'
    allowed_methods = ['get', 'post']

    def get_object(self, **kwargs):
        return Order.objects.get(url=kwargs['url'])

    def post(self, *args, **kwargs):

        return HttpResponseRedirect(reverse(''))


def receive_success(request):
    return render(request, 'success.html')


class GiftListView(ListView):
    model = Order
    template_name = 'list.html'
    allowed_methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse(''))

    def post(self, request, *args, **kwargs):
        value = request.POST.get('value', '')
        order = Order.objects.get(id=int(value))
        attrs = {}
        url = 'https://dev-change.net/recieve/' + order.gift_url
        attrs.update({
            'orderer_name': order.orderer_name,
            'reciever_phone': order.reciever_phone,
            'url': url
            })
        self.send_code(attrs)
        return super().post(request, *args, **kwargs)

    def send_code(self, attrs):
        body = f'''[Web 발신]
        띵-동! {attrs['orderer_name']} 님으로부터 선물이 도착했어요!🎁
        {attrs['orderer_name']} 님의 진심이 가득한 선물과 편지 확인하러 가기!🏃
        {attrs['url']}
        '''
        PhoneLog.objects.create(to=attrs['reciever_phone'], body=body)


def gifter(request):
    if request.method == 'GET':
        return render(request, 'gifter.html')
    if request.method == 'POST':
        orderer_name = request.POST.get('orderer_name', '')
        orderer_phone = request.POST.get('orderer_phone', '')
        reciever_name = request.POST.get('reciever_name', '')
        reciever_phone = request.POST.get('reciever_phone', '')
        gift_reason = request.POST.get('gift_reason', '')
        message = request.POST.get('message', '')
        current_datetime = datetime.datetime.now()
        hash_string = orderer_name + orderer_phone + str(current_datetime.timestamp())
        url = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()
        try:
            order = Order.models.get(orderer_phone=orderer_phone)
            order.gift_reason = gift_reason
            order.message = message
            order.orderer_name = orderer_name
            order.orderer_phone = orderer_phone
            order.reciever_name = reciever_name
            order.reciever_phone = reciever_phone
            order.gift_url = url
        except:
            order = Order.objects.create(
                orderer_phone=orderer_phone,
                orderer_name=orderer_name,
                reciever_phone=reciever_phone,
                reciever_name=reciever_name,
                gift_reason=gift_reason,
                message=message
            )
        order.save()
        request.session['name'] = orderer_name
        return redirect('gift_success')


def gift_success(request):
    return render(request, 'gift_success.html')
