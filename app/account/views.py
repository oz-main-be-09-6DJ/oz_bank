from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from account.models import Account
from account.serializers import AccountCreateSerializer,AccountReadSerializer,AccountUpdateSerializer
from rest_framework import status
from rest_framework.response import Response

class AccountListCreateAPIView(ListCreateAPIView):#계좌 생성 API (로그인한 사용자만 가능)
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).order_by("id")  # 본인 계좌만 조회

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AccountCreateSerializer
        return AccountReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 계좌 생성 시 유저 자동 지정

class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):#한 계좌 조회, 수정, 삭제 API
    serializer_class = AccountReadSerializer  # 기본적으로 조회용 Serializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)  # 본인 계좌만 접근 가능

    def get_serializer_class(self):#PATCH 또는 PUT 요청이면 수정용 Serializer 사용
        if self.request.method in ['PUT', 'PATCH']:
            return AccountUpdateSerializer
        return AccountReadSerializer
    def perform_destroy(self, instance):#본인 계좌만 삭제 가능하도록 설정, 잔액이 0원이어야 함
        if instance.user != self.request.user:
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if instance.balance > 0:
            return Response({"detail": "잔액이 0원이 아닌 계좌는 삭제할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
    def delete(self, request, *args, **kwargs):#DELETE 요청 시 JSON 응답 반환 <--postman으로 해보니까 삭제되면 json안날라오길래 오버라이딩 했어요
        account = self.get_object()
        account.delete()
        return Response({"message": "계좌가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)