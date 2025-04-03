from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


# Custom User(유저) 모델
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=50, null=False)
    nickname = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    password = models.TextField(null=False) # AbstractBaseUser가 password 해싱 처리
    type = models.CharField(max_length=10, choices=[("admin", "Admin"), ("user", "User")], default="user")
    authentication = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"  # 로그인할 때 사용할 필드
    EQUIRED_FIELDS = ["name", "nickname", "phone_number"]   # `createsuperuser` 명령어 실행할 때 필수 필드

    # __str__() -> print(user) 하면 이메일이 출력됨
    def __str__(self):
        return self.email