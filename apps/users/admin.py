from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "nickname", "phone_number", "is_staff", "is_active")  # 관리자 페이지에서 보이는 컬럼
    list_filter = ("is_staff", "is_active")  # 필터링 옵션 추가
    search_fields = ("email", "nickname", "phone_number")  # 검색 기능 활성화
    ordering = ("email",)  # 정렬 기준 설정
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "nickname", "phone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "create_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "nickname", "phone_number", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)