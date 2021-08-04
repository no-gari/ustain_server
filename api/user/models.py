from django.contrib.auth.models import Group as AuthGroup, AbstractUser, UserManager as DjangoUserManager
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


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
    REQUIRED_FIELDS = []
    VERIFY_FIELDS = ['phone']  # 회원가입 시 검증 받을 필드 (email, phone)
    REGISTER_FIELDS = ['email', 'password']  # 회원가입 시 입력 받을 필드 (email, phone, password)

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


class UserGroup(models.Model):
    group = models.OneToOneField(AuthGroup, unique=True, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='이미지', blank=True, null=True)

    def __str__(self):
        return "{}".format(self.group.name)


class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name='카테고리 이름', help_text='카테고리 이름을 입력하세요.')
    mid = models.CharField(unique=True, max_length=255, verbose_name='카테고리 고유값',
                           help_text='영문+숫자 조합만 가능한 카테고리의 고유값입니다.')
    description = models.TextField(blank=True, null=True, verbose_name='카테고리 설명', help_text='카테고리에 대한 간단한 설명을 입력합니다.')
    snapshot_image = models.ImageField(blank=True, null=True, verbose_name='이미지', help_text='해당하는 이미지 파일을 선택하세요.')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='닉네임', max_length=32, default='anonymous user')
    groups = models.ManyToManyField(UserGroup, verbose_name='속한 그룹')
    profile_article = models.CharField(max_length=512, verbose_name='프로필 정보', null=True, blank=True)
    birthday = models.DateField(verbose_name='생일', null=True, blank=True)
    categories = models.ManyToManyField(Categories, verbose_name='관심 카테고리')

    class SexChoices(models.TextChoices):
        MALE = 'MA', _('남자')
        FEMALE = 'FE', _('여자')

    sex_choices = models.CharField(
        max_length=2,
        choices=SexChoices.choices,
        default=SexChoices.MALE,
    )

    def __str__(self):
        return self.user.username + ' 의 프로필'

    @receiver(models.signals.post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.create(user=instance)
            profile.save()


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
