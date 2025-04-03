
from django.urls import path
from users.views import *
from users.jwt_view import UserSignUpAPIView
app_name='users_noti_api'

urlpatterns=[
    path("",UserSignUpAPIView.as_view(),name="user_signup"),
]