from django.test import TestCase  # Django의 테스트 프레임워크
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import CustomUser, EmailVerificationToken
#CustomUser model 테스트
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
        
#회원가입,이메일 인증,로그인token발급,로그아웃refresh token blacklist등록,회원정보 수정/삭제 테스트
class UserSignUpAPIView_VerifyEmailView_TestCase(TestCase):
    def setUp(self):
        # user_data 정의
        self.client = APIClient()  # APIClient로 변경
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'name': 'Test User',
            'nickname': 'Tester',
            'phone_number': '010-1234-5678',
        }
        # 기존의 모든 이메일 인증 토큰을 삭제
        EmailVerificationToken.objects.all().delete()
        
        # 사용자 및 토큰 생성
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.token = EmailVerificationToken.objects.create(user=self.user)
    
    
    def test_login(self):
        """로그인 API 테스트"""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(reverse('users_noti_api:user_login'), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # access token이 응답에 포함되어야 함
        self.assertIn('refresh', response.data)  # refresh token이 응답에 포함되어야 함
        
        
    def test_profile_delete(self):
        """유저 프로필 삭제 API 테스트"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('users_noti_api:user_profile'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # 삭제된 유저의 deleted_at 필드가 설정되었는지 확인
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.deleted_at)

    def test_logout(self):
        """로그아웃 API 테스트 (refresh token blacklist 등록)"""
        # 로그인 후 refresh token을 받는다.
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(reverse('users_noti_api:user_login'), login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # 로그아웃 요청 전에 force_authenticate로 인증 처리
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')

        response = self.client.post(reverse('users_noti_api:user_logout'), {'refresh_token': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)