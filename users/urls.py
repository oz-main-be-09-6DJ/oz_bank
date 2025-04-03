
from django.urls import path
from users.views import *
from users.jwt_view import UserSignUpAPIView,UserMeAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
app_name='users_noti_api'

urlpatterns=[
    path("",UserSignUpAPIView.as_view(),name="user_signup"),
    path("login/",TokenObtainPairView.as_view(),name="user_login"),
    path("profile/",UserMeAPIView.as_view(),name="user_profile"),
]