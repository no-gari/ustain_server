from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.user.views import UserRegisterView, EmailVerifierCreateView, EmailVerifierConfirmView, \
    PhoneVerifierCreateView, PhoneVerifierConfirmView, UserSocialLoginView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('social-login/', UserSocialLoginView.as_view()),
    path('register/', UserRegisterView.as_view()),
    # path('email-verifier/', EmailVerifierCreateView.as_view()),
    # path('email-verifier/confirm/', EmailVerifierConfirmView.as_view()),
    path('phone-verifier/', PhoneVerifierCreateView.as_view()),
    path('phone-verifier/confirm/', PhoneVerifierConfirmView.as_view()),
]