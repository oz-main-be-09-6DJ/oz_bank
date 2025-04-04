
from django.urls import path
from apps.account.views import AccountListCreateAPIView, AccountDetailAPIView

app_name='account_api'

urlpatterns=[
    path('', AccountListCreateAPIView.as_view(), name='list_create'),#조회,생성
    path('<int:pk>/', AccountDetailAPIView.as_view(), name='detail')#삭제,상세조회
]