from rest_framework import permissions

# 특정 유저가 블로그 글을 삭제 하고, 수정 하고, 삭제할 수 있는 사람을 정의하기 위한 클래스
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            # APIView 사용시
            obj = view.get_object(request, *view.args, **view.kwargs)
        except TypeError:
            # DRF Generic 사용시
            obj = view.get_object()
        return obj.author == request.user