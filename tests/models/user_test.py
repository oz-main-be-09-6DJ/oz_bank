from django.test import TestCase  # Django의 테스트 프레임워크
from users.models import CustomUser  # User 모델을 가져옴
from django.utils import timezone


class TestCustomUserModel(TestCase):
    """CustomUser 모델의 동작을 검증하는 테스트"""

    def setUp(self):
        """Given: 테스트에 필요한 유저 생성"""
        self.user = CustomUser.objects.create(
            email="test@example.com",  # 이메일 (로그인 ID)
            name="Test User",  # 이름
            nickname="Tester",  # 닉네임
            phone_number="010-1234-5678",  # 전화번호
            password="securepassword123",  # 비밀번호 (해싱 X, `AbstractBaseUser`가 내부적으로 관리)
        )

    def test_user_creation(self):
        """When: 유저를 생성했을 때 Then: 정상적으로 저장되는지 확인"""

        # 유저가 정상적으로 생성되었는지 확인
        user = CustomUser.objects.get(email="test@example.com")  # 이메일 기준 조회
        self.assertIsNotNone(user)  # user 객체가 None이 아닌지 확인

        # 저장된 유저의 필드 값이 올바른지 검증
        self.assertEqual(user.name, "Test User")  # 이름 확인
        self.assertEqual(user.nickname, "Tester")  # 닉네임 확인
        self.assertEqual(user.phone_number, "010-1234-5678")  # 전화번호 확인
        self.assertEqual(user.type, "user")  # 기본값이 "user"인지 확인
        self.assertFalse(user.authentication)  # 기본값 False인지 확인
        self.assertFalse(user.notification)  # 기본값 False인지 확인
        self.assertIsNone(user.deleted_at)  # 기본적으로 삭제되지 않은 상태인지 확인

    def test_user_string_representation(self):
        """When: User 객체를 문자열로 변환할 때 Then: 이메일이 반환되는지 확인"""

        expected_str = "test@example.com"  # `__str__()` 메서드가 이메일을 반환하는지 확인
        self.assertEqual(str(self.user), expected_str)

    def test_user_soft_delete(self):
        """When: 유저를 삭제했을 때 Then: `deleted_at` 필드가 설정되는지 확인"""

        self.user.deleted_at = timezone.now()  # 삭제된 시간 설정
        self.user.save()

        user = CustomUser.objects.get(email="test@example.com")
        self.assertIsNotNone(user.deleted_at)  # 삭제 시간이 설정되었는지 확인

    def test_default_user_type(self):
        """When: 유저 생성 시 Then: 기본 `type`이 'user'인지 확인"""

        self.assertEqual(self.user.type, "user")  # 기본값이 "user"인지 확인

    def test_user_authentication_toggle(self):
        """When: `authentication` 값을 변경할 때 Then: 값이 정상적으로 변경되는지 확인"""

        self.user.authentication = True  # 인증 완료 상태로 변경
        self.user.save()

        user = CustomUser.objects.get(email="test@example.com")
        self.assertTrue(user.authentication)  # 변경된 값 확인
