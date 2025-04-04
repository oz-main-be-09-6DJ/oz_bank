from django.core.mail import send_mail
from django.conf import settings
from users.models import EmailVerificationToken
from django.utils.crypto import get_random_string

def send_verification_email(user):
    """
    사용자에게 이메일 인증 메일을 보냄
    """
    # 토큰 생성
    token_obj, created = EmailVerificationToken.objects.get_or_create(user=user)
    token_obj.token = get_random_string(length=64)  # 64자리 랜덤 문자열 생성
    token_obj.save()

    verification_url = f"http://127.0.0.1:8000/api/auth/verify-email/{token_obj.token}/"

    subject = "이메일 인증을 완료해주세요"
    message = f"안녕하세요, {user.name}님!\n이메일 인증을 완료하려면 아래 링크를 클릭해주세요.\n\n{verification_url}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
