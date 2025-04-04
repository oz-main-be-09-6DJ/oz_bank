from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView,CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from account.models import Account
from account.serializers import AccountCreateSerializer,AccountReadSerializer,AccountUpdateSerializer

class AccountCreateAPIView(CreateAPIView):#계좌 생성 API (로그인한 사용자만 가능)
    serializer_class = AccountCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)#현재 로그인한 유저를 계좌 주인으로 설정

class AccountListAPIView(ListAPIView):#원래 로그인한 사용자의 모든 계좌 조회 API
    serializer_class = AccountReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):# 본인 계좌만 조회 가능하도록 오버로딩
        return Account.objects.filter(user=self.request.user)

class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):#한 계좌 조회, 수정, 삭제 API
    serializer_class = AccountReadSerializer  # 기본적으로 조회용 Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)  # 본인 계좌만 접근 가능

    def get_serializer_class(self):#PATCH 또는 PUT 요청이면 수정용 Serializer 사용
        if self.request.method in ['PUT', 'PATCH']:
            return AccountUpdateSerializer
        return AccountReadSerializer