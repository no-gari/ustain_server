from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.user.views.register import UserRegisterView, PhoneVerifierCreateView, \
    PhoneVerifierConfirmView
from api.user.views.login import UserSocialLoginView
from api.user.views.email import EmailVerifierCreateView, EmailVerifierConfirmView, EmailFoundPhoneVerifierCreateView, \
    EmailFoundPhoneVerifierConfirmView
from api.user.views.update import UserUpdateView, PhoneUpdateVerifierCreateView, PhoneUpdateVerifierConfirmView, \
    PasswordResetVerifyView, PasswordResetConfirmView, PasswordResetView


urlpatterns = [
    # 이메일 회원가입, 로그인
    path('register/', UserRegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    # 소셜 로그인
    path('social-login/', UserSocialLoginView.as_view()),
    path('email-verifier/', EmailVerifierCreateView.as_view()),
    path('email-verifier/confirm/', EmailVerifierConfirmView.as_view()),
    path('phone-verifier/', PhoneVerifierCreateView.as_view()),
    path('phone-verifier/confirm/', PhoneVerifierConfirmView.as_view()),
    path('email-found/phone-verifier/', EmailFoundPhoneVerifierCreateView.as_view()),
    path('email-found/phone-verifier/confirm/', EmailFoundPhoneVerifierConfirmView.as_view()),
    path('password-reset/', PasswordResetVerifyView.as_view()),
    path('password-reset/<str:code>/<str:email_token>/', PasswordResetView.as_view()),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('update/phone/phone-verifier/', PhoneUpdateVerifierCreateView.as_view()),
    path('update/phone/phone-verifier/confirm/', PhoneUpdateVerifierConfirmView.as_view()),
    path('update/<str:email>/', UserUpdateView.as_view()),
]
