from django.urls import path
from transaction.views import *

app_name = 'transaction_api'

urlpatterns = [
    # 거래 내역 리스트 조회 및 생성 API
    path('transactions/list/', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),

    # 거래 내역 조회, 수정, 삭제 API (PK로 특정 거래를 조회)
    path('transactions/detail/<int:pk>/', TransactionRetrieveUpdateDestroyAPIView.as_view(),
         name='transaction-retrieve-update-destroy'),
]