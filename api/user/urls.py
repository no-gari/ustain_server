from django.urls import path
from api.user.views.update import UserProfileView, PhoneUpdateVerifierCreateView, PhoneUpdateVerifierConfirmView, \
    PasswordResetVerifyView, PasswordResetConfirmView, PasswordResetView
from api.user.views.email import EmailVerifierCreateView, EmailFoundPhoneVerifierCreateView, \
    EmailFoundPhoneVerifierConfirmView
from api.user.views.login import UserSocialLoginView, CustomTokenObtainPairView, CustomTokenRefreshView
from api.user.views.register import UserRegisterView, PhoneVerifierCreateView, PhoneVerifierConfirmView
from api.user.views.category import CategoryListView
<<<<<<< HEAD
from api.user.views.clayful_api import ClayfulRegisterView, ClayfulLoginView
=======
>>>>>>> 4f5acb9637fb95e61c628f9b776db51d52291047

urlpatterns = [
    # 이메일 회원가입, 로그인
    path('register/', UserRegisterView.as_view()),
<<<<<<< HEAD
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    # clayful 회원가입, 로그인
    path('clayful/register/', ClayfulRegisterView.as_view()),
    path('clayful/login/', ClayfulLoginView.as_view()),
=======
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', CustomTokenRefreshView.as_view()),
>>>>>>> 4f5acb9637fb95e61c628f9b776db51d52291047

    # 소셜 로그인
    path('social-login/', UserSocialLoginView.as_view()),

    # 이메일 중복 확인
    path('email-verifier/', EmailVerifierCreateView.as_view()),

    # 휴대폰 코드 인증
    path('phone-verifier/', PhoneVerifierCreateView.as_view()),
    path('phone-verifier/confirm/', PhoneVerifierConfirmView.as_view()),

    # 이메일 찾기 -> 휴대폰 인증
    path('email-found/phone-verifier/', EmailFoundPhoneVerifierCreateView.as_view()),
    path('email-found/phone-verifier/confirm/', EmailFoundPhoneVerifierConfirmView.as_view()),

    # 유저 프로필 가져오기, 업데이트, 삭제
    path('profile/', UserProfileView.as_view()),

    # 카테고리 전체 가져오기
    path('categories/', CategoryListView.as_view()),

    # 비밀번호 재설정 링크
    path('password-reset/', PasswordResetVerifyView.as_view()),
    path('password-reset/<str:code>/<str:email_token>/', PasswordResetView.as_view()),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # 휴대폰 번호 재설정
    path('update/phone/phone-verifier/', PhoneUpdateVerifierCreateView.as_view()),
    path('update/phone/phone-verifier/confirm/', PhoneUpdateVerifierConfirmView.as_view()),
]