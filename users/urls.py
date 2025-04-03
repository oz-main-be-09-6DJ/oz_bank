from django.urls import path
from users.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name='users_noti_api'

urlpatterns = [
    path("auth/verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("users/signup/",UserSignUpAPIView.as_view(),name="user_signup"),
    path("users/login/",TokenObtainPairView.as_view(),name="user_login"),
    path("users/profile/",ProfileView.as_view(),name="user_profile"),
    path('users/logout/', LogoutView.as_view(), name='user_logout'),#api/users/logout
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#api/token/refresh POST
]