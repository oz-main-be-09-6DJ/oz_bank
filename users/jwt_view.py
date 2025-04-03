from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from users.serializers import UserSignUpSerializer,UserUpdateMeSerializer,UserReadMeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
class UserSignUpAPIView(CreateAPIView):
    serializer_class=UserSignUpSerializer
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