from django.contrib.auth.models import Group as AuthGroup, AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserGroup(models.Model):
    group = models.OneToOneField(AuthGroup, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='이미지', blank=True, null=True)

    def __str__(self):
        return "{}".format(self.group.name)


class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name='카테고리 이름', help_text='카테고리 이름을 입력하세요.')
    mid = models.CharField(unique=True, max_length=255, verbose_name='카테고리 고유값',
                           help_text='영문+숫자 조합만 가능한 카테고리의 고유값입니다.', primary_key=True)
    description = models.TextField(blank=True, null=True, verbose_name='카테고리 설명', help_text='카테고리에 대한 간단한 설명을 입력합니다.')
    snapshot_image = models.ImageField(blank=True, null=True, verbose_name='이미지', help_text='해당하는 이미지 파일을 선택하세요.')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '소셜 카테고리'
        verbose_name_plural = '소셜 카테고리'


class UserManager(DjangoUserManager):
    def _create_user(self, phone, password, **extra_fields):
        phone = self.model.normalize_username(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    name = models.CharField(verbose_name='닉네임', max_length=16, null=True, blank=True)
    email = models.EmailField(verbose_name='이메일', null=True, blank=True)
    email_verify = models.BooleanField(verbose_name='이메일 인증', default=False)
    phone = models.CharField(verbose_name='휴대폰', max_length=11, unique=True)
    groups = models.ManyToManyField(UserGroup, verbose_name='속한 그룹', null=True, blank=True)
    profile_article = models.CharField(max_length=512, verbose_name='프로필 정보', null=True, blank=True)
    birthday = models.DateField(verbose_name='생일', null=True, blank=True)
    categories = models.ManyToManyField(Categories, verbose_name='관심 카테고리')
    points = models.IntegerField(verbose_name='포인트', default=0)

    class SexChoices(models.TextChoices):
        MALE = 'MA', _('남자')
        FEMALE = 'FE', _('여자')

    sex_choices = models.CharField(
        max_length=2,
        choices=SexChoices.choices,
        default=SexChoices.MALE,
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    VERIFY_FIELDS = ['phone']  # 회원가입 시 검증 받을 필드 (email, phone)
    REGISTER_FIELDS = ['phone', 'password']  # 회원가입 시 입력 받을 필드 (phone, password)

    objects = UserManager()

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.phone

    @property
    def is_social(self):
        return hasattr(self, 'social')


class EmailVerifier(models.Model):
    email = models.EmailField(verbose_name='이메일')
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')

    class Meta:
        verbose_name = '이메일 중복 확인'
        verbose_name_plural = verbose_name


class PhoneVerifier(models.Model):
    phone = models.CharField(verbose_name='휴대폰번호', max_length=11)
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')

    class Meta:
        verbose_name = '휴대폰 인증'
        verbose_name_plural = verbose_name
