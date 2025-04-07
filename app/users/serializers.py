from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import CustomUser,Notification

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "name", "nickname", "phone_number", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # AUTH_PASSWORD_VALIDATORS 과 관련된 로직을 읽기 위한 메서드이며,
    # validate_password(password=data['password'], user=user) 로 패스워드 유효성 검사
    def validate(self, data):
        user = CustomUser(**data)
        errors = dict()
        try:
            validate_password(password=data['password'], user=user)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return super().validate(data)
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class UserReadMeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields="__all__"
        
class UserUpdateMeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=["name","phone_number","notification","password"]
    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
    
