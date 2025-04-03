from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import CustomUser,Notification

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = [
            "email",
            "name",
            "nickname",
            "phone_number",
            "password",
            "type",
            "notification",
        ]
        
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
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
    
