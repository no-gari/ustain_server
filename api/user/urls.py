from api.user.views.update import UserProfileView, PhoneUpdateVerifierCreateView, PhoneUpdateVerifierConfirmView
from api.user.views.email import PasswordChangeVerifierConfirmView, PasswordChangeVerifierCreateView
from api.user.views.register import UserRegisterView, PhoneVerifierCreateView, PhoneVerifierConfirmView
from api.user.views.login import CustomTokenObtainPairView, CustomTokenRefreshView
from api.user.views.category import CategoryListView
from django.urls import path


urlpatterns = [
    # 이메일 회원가입, 로그인
    path('register/', UserRegisterView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', CustomTokenRefreshView.as_view()),

    # 휴대폰 코드 인증
    path('phone-verifier/', PhoneVerifierCreateView.as_view()),
    path('phone-verifier/confirm/', PhoneVerifierConfirmView.as_view()),

    # 비밀번호 리셋 -> 휴대폰 인증
    path('password-reset/phone-verifier/', PasswordChangeVerifierCreateView.as_view()),
    path('password-reset/phone-verifier/confirm/', PasswordChangeVerifierConfirmView.as_view()),

    # 유저 프로필 가져오기, 업데이트, 삭제
    path('profile/', UserProfileView.as_view()),

    # 카테고리 전체 가져오기
    path('categories/', CategoryListView.as_view()),


    # 휴대폰 번호 재설정
    path('update/phone/phone-verifier/', PhoneUpdateVerifierCreateView.as_view()),
    path('update/phone/phone-verifier/confirm/', PhoneUpdateVerifierConfirmView.as_view()),
]
