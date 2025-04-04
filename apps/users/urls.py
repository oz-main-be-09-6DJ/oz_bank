from django.urls import path
from apps.users.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import oauth_views

app_name='users_noti_api'

urlpatterns = [
    path("auth/verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("users/signup/",UserSignUpAPIView.as_view(),name="user_signup"),
    path("users/login/",TokenObtainPairView.as_view(),name="user_login"),
    path("users/profile/",ProfileView.as_view(),name="user_profile"),
    path('users/logout/', LogoutView.as_view(), name='user_logout'),#api/users/logout
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#api/token/refresh POST

    # oauth naver
    path('naver/login-page/', oauth_views.naver_login_page, name='naver_login_page'),  # 로그인 버튼 있는 페이지
    path('naver/login/', oauth_views.NaverLoginRedirectView.as_view(), name='naver_login'),
    path('naver/callback/', oauth_views.naver_callback, name='naver_callback'),
]