from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import UserUpdateMeSerializer, UserReadMeSerializer
from django.utils import timezone

# 유저프로필 조회, 수정, 삭제 뷰
class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 접근

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserUpdateMeSerializer # 유저 프로필 수정
        return UserReadMeSerializer # 유저 프로필 조회

    # 유저 프로필 삭제 (삭제일자 저장, 비활성화 상태?)
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted_at = timezone.now()
        user.save(update_fields=['deleted_at'])

        return Response({"message":"Delete successfully"},status=status.HTTP_204_NO_CONTENT)


