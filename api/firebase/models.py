from django.db import models
from api.user.models import User


class PushToken(models.Model):
    token = models.CharField(verbose_name='토큰', max_length=200)
    user = models.ForeignKey(User , verbose_name='유저', on_delete=models.CASCADE, related_name='tokens')

    def __str__(self):
        return f'{self.user}'
