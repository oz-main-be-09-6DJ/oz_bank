from rest_framework.generics import CreateAPIView
from users.models import CustomUser
from users.serializers import UserUpdateMeSerializer,UserSignUpSerializer,UserReadMeSerializer
class UserSignUpAPIView(CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserSignUpSerializer