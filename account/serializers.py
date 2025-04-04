from rest_framework import serializers
from account.models import Account
from users.serializers import UserReadMeSerializer

class AccountCreateSerializer(serializers.ModelSerializer):
    user=UserReadMeSerializer(read_only=True)#계정 주인 임의 변경 불가
    balance = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    class Meta:
        model=Account
        fields=[ 'account_number','bank_code','account_type','balance','user']
    def create(self,validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("로그인이 필요합니다.")
        validated_data['user'] = request.user
        return super().create(validated_data)
    
class AccountReadSerializer(serializers.ModelSerializer):
    user=UserReadMeSerializer(read_only=True)
    balance = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)
    class Meta:
        model=Account
        fields="__all__"
        
class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['balance']