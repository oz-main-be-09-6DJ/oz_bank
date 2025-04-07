from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string


# User 모델을 관리하는 Manager (create_user, create_superuser()를 직접 구현하기 위해)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 입력 항목입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱 처리
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("phone_number"):
            raise ValueError("Superuser는 phone_number를 반드시 입력해야 합니다.")

        return self.create_user(email, password, **extra_fields)

# Custom User(유저) 모델
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=50, null=False)
    nickname = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    password = models.TextField(null=False)  # AbstractBaseUser가 password 해싱 처리
    type = models.CharField(max_length=10, choices=[("admin", "Admin"), ("user", "User")], default="user")
    authentication = models.BooleanField(default=False)
    notification = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)  # 사용자 활성화 여부
    is_staff = models.BooleanField(default=False)  # Django Admin 접근 여부

    objects = CustomUserManager()  # ✅ UserManager 설정

    USERNAME_FIELD = "email"  # 로그인할 때 사용할 필드
    REQUIRED_FIELDS = ["name", "nickname", "phone_number"]  # `createsuperuser` 명령어 실행할 때 필수 필드

    # __str__() -> print(user) 하면 이메일이 출력됨
    def __str__(self):
        return self.email

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="email_token")
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_token(self):
        self.token = get_random_string(length=64)
        self.save()

# 특정 사용자(CustomUser)의 알림을 저장하고 관리할 수 있음
class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,   # 사용자가 삭제되면 해당 알림도 함꼐 삭제됨
        db_column="user_id",
        related_name="notifications"  # 기본 "notification_set" 대신 "notifications" 사용
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.message}"