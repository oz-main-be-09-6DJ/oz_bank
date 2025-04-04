
from django.urls import path
from account.views import *

app_name='account_api'

urlpatterns=[
    path('', AccountListAPIView.as_view(), name='account-list'),#조회
    path('create/', AccountCreateAPIView.as_view(), name='account-create'),#생성
    path('<int:pk>/', AccountDetailAPIView.as_view(), name='account-detail')#삭제,상세조회
]