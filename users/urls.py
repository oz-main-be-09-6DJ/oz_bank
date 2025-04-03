from django.urls import path
from users.views import *

app_name='users_noti_api'

urlpatterns=[
    path("user/profile", ProfileView.as_view(), name="profile"),
]