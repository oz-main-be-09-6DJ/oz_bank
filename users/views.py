from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from users.serializers import UserSignUpSerializer,UserUpdateMeSerializer,UserReadMeSerializer
from utils.email import send_verification_email
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import EmailVerificationToken

CustomUser = get_user_model()

class UserSignUpAPIView(CreateAPIView):
    serializer_class=UserSignUpSerializer
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


# GET: 회원 정보 확인 / PATCH: 회원 정보 수정
class UserMeAPIView(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get_object(self):
        return self.request.user
    def get_serializer_class(self):
        if self.request.method=='GET':
            return UserReadMeSerializer
        elif self.request.method=='PATCH':
            return UserUpdateMeSerializer

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