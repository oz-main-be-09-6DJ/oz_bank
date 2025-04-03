from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import EmailVerificationToken
from users.serializers import UserSignUpSerializer, UserUpdateMeSerializer, UserReadMeSerializer
from utils.email import send_verification_email

CustomUser = get_user_model()


class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 회원가입 성공 후 이메일 인증 메일 발송
        send_verification_email(user)

        return Response(
            {"message": "회원가입이 완료되었습니다. 이메일을 확인하고 인증을 진행해주세요."},
            status=status.HTTP_201_CREATED
        )


# 유저프로필 조회, 수정, 삭제 뷰
class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserUpdateMeSerializer  # 유저 프로필 수정
        return UserReadMeSerializer  # 유저 프로필 조회

    # 유저 프로필 삭제 (삭제일자 저장, 비활성화 상태?)
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted_at = timezone.now()
        user.save(update_fields=['deleted_at'])

        return Response({"message": "Delete successfully"}, status=status.HTTP_204_NO_CONTENT)


# 이메일 인증 완료 처리
class VerifyEmailView(generics.GenericAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, token):
        try:
            token_obj = EmailVerificationToken.objects.get(token=token)
            user = token_obj.user
            user.authentication = True  # ✅ 이메일 인증 완료
            user.save()
            token_obj.delete()  # 사용한 토큰 삭제

            return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)

        except EmailVerificationToken.DoesNotExist:
            return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")  # 요청에서 Refresh Token 가져오기
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 추가

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
