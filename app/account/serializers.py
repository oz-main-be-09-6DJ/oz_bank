from rest_framework import serializers
from account.models import Account
from users.serializers import UserReadMeSerializer
from decimal import Decimal
class AccountCreateSerializer(serializers.ModelSerializer):
    user=UserReadMeSerializer(read_only=True)#계정 주인 임의 변경 불가
    balance = serializers.DecimalField(max_digits=18, decimal_places=2, required=False)
    class Meta:
        model=Account
        fields=[ 'account_number','bank_code','account_type','balance','user']
    def create(self,validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("로그인이 필요합니다.")
        validated_data['user'] = request.user
        balance = validated_data.pop('balance', Decimal("0.00"))  # balance가 없으면 기본값 0.00
        account = Account.objects.create(balance=balance, **validated_data)  # balance 저장
        return account
    def to_representation(self, instance):#Response의 user 필드에서 name만 포함하도록 수정
        data = super().to_representation(instance)  # 기존 직렬화된 데이터 가져오기
        if instance.user:  # user가 존재하는 경우
            data['user'] = {'name': instance.user.name}  # user 필드에 name만 포함
        return data
    
class AccountReadSerializer(serializers.ModelSerializer):
    user=UserReadMeSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    class Meta:
        model=Account
        fields="__all__"
    def to_representation(self, instance):#Response의 user 필드에서 name만 포함하도록 수정
        data = super().to_representation(instance)  # 기존 직렬화된 데이터 가져오기
        if instance.user:  # user가 존재하는 경우
            data['user'] = {'name': instance.user.name}  # user 필드에 name만 포함
        return data
        
class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['balance']