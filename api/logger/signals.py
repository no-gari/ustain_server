import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from api.logger.models import EmailLog, PhoneLog


@receiver(post_save, sender=EmailLog)
def send_mail_gun(sender, instance, created, *args, **kwargs):
    if created:
        url = f'https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages'
        headers = {
            'Authorization': f'api {settings.MAILGUN_API_KEY}'
        }
        data = {
            'from': settings.MAILGUN_FROM_EMAIL,
            'to': [instance.to],
            'subject': instance.title,
            'html': instance.body,
        }
        response = requests.request(method='post', url=url, headers=headers, data=data)
        if response.status_code != 200:
            instance.status = 'F'
        else:
            instance.status = 'S'
        instance.save()


@receiver(post_save, sender=PhoneLog)
def send_sms(sender, instance, created, *args, **kwargs):
    if created:
        api_key = settings.COOLSMS_API_KEY
        api_secret = settings.COOLSMS_API_SECRET
        # 문자 전송
        data = {
            'from': settings.COOLSMS_FROM_PHONE,
            'to': instance.to,
            'text': instance.body,
        }

        message = Message(api_key, api_secret, use_http_connection=True)
        try:
            response = message.send(data)
            if 'error_list' in response:
                instance.fail_reason = str(response)
            if response['success_count']:
                instance.status = 'S'
            else:
                instance.status = 'F'
                instance.fail_reason = str(response)

        except CoolsmsException as e:
            instance.status = 'F'
            instance.fail_reason = e.msg
        instance.save()
