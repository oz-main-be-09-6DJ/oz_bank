from rest_framework import serializers
from .models import Transaction

# 거래 내역을 직렬화하는 클래스
class TransactionSerializer(serializers.ModelSerializer):
    # Account 모델의 'account_number', 'bank_name', 'account_type_name' 필드를 거래 내역에 포함
    account_number = serializers.CharField(source='account.account_number', read_only=True)
    bank_name = serializers.CharField(source='account.bank_name', read_only=True)
    account_type_name = serializers.CharField(source='account.account_type_name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'transaction_method', 'transaction_amount', 'transaction_balance',
                  'transaction_details', 'created_date', 'account_number', 'bank_name', 'account_type_name']
        read_only_fields = ['created_date', 'account_number', 'bank_name', 'account_type_name']  # 수정 불가 필드