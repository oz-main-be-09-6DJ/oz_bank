from rest_framework import generics, permissions, serializers
from account.models import Account
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters


# 거래 내역에 대한 필터링 조건을 정의한 클래스
class TransactionFilter(filters.FilterSet):
    transaction_type = filters.CharFilter(field_name='transaction_type', lookup_expr='exact')  # 거래 유형 필터
    transaction_method = filters.CharFilter(field_name='transaction_method', lookup_expr='exact')  # 거래 방법 필터
    min_amount = filters.NumberFilter(field_name='transaction_amount', lookup_expr='gte')  # 최소 금액 필터
    max_amount = filters.NumberFilter(field_name='transaction_amount', lookup_expr='lte')  # 최대 금액 필터
    created_date = filters.DateTimeFilter(field_name='created_date', lookup_expr='gte')  # 생성된 날짜 이후 필터

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'transaction_method', 'min_amount', 'max_amount', 'created_date']


# 거래 내역 리스트 조회 및 생성 API

class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        account_number = self.request.data.get('account_number')
        if not account_number:
            raise serializers.ValidationError({"account_number": "이 필드는 필수 항목입니다."})

        try:
            account = Account.objects.get(account_number=account_number, user=self.request.user)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"account_number": "해당 계좌가 존재하지 않거나, 본인의 계좌가 아닙니다."})

        # trader는 User 객체가 아닌 user.id (정수)로 넣기!
        serializer.save(account=account, trader=self.request.user.id)

# 거래 내역 조회, 수정, 삭제 API
class TransactionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()  # 모든 거래 내역을 기본 쿼리셋으로 사용
    serializer_class = TransactionSerializer  # 거래 내역을 직렬화할 Serializer 사용
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    # 거래 내역 객체를 조회하는 메소드 (기본적으로 pk로 객체를 가져옴)
    def get_object(self):
        return super().get_object()  # 부모 클래스의 메소드 호출로 객체 조회