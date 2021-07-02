from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.model.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(verbose_name='이메일', unique=True)
    phone = models.CharField(verbose_name='휴대폰', max_length=11, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    VERIFY_FIELDS = []  # 회원가입 시 검증 받을 필드 (email, phone)
    REGISTER_FIELDS = ['phone', 'password']  # 회원가입 시 입력 받을 필드 (email, phone, password)

    objects = UserManager()

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class SocialKindChoices(models.TextChoices):
    KAKAO = 'kakao', '카카오'
    NAVER = 'naver', '네이버'
    FACEBOOK = 'facebook', '페이스북'
    GOOGLE = 'google', '구글'
    APPLE = 'apple', '애플'


class Social(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)
    kind = models.CharField(verbose_name='타입', max_length=16, choices=SocialKindChoices.choices)

    class Meta:
        verbose_name = '소셜'
        verbose_name_plural = verbose_name


class EmailVerifier(models.Model):
    email = models.EmailField(verbose_name='이메일')
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')


class PhoneVerifier(models.Model):
    phone = models.CharField(verbose_name='휴대폰번호', max_length=11)
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')
