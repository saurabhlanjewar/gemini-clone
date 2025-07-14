from django.urls import path
from .views import *

urlpatterns = [
    path("auth/signup", SignupView.as_view()),
    path("auth/send-otp", SendOTPView.as_view()),
    path("auth/verify-otp", VerifyOTPView.as_view()),
    path("auth/forgot-password", ForgotPasswordOTPView.as_view()),
    path("auth/change-password", ChangePasswordView.as_view()),
    path("user/me", CurrentUserView.as_view()),
]
