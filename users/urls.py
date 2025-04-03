from django.urls import path
from users.views import *
from users.jwt_view import UserSignUpAPIView,UserMeAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

app_name='users_noti_api'

urlpatterns = [
    path("users/register/", UserRegistrationView.as_view(), name="user-register"),
    path("users/auth/verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("users/signup/",UserSignUpAPIView.as_view(),name="user_signup"),
    path("users/login/",TokenObtainPairView.as_view(),name="user_login"),
    path("users/profile/",UserMeAPIView.as_view(),name="user_profile"),
]