import requests
from django.conf import settings
from django.contrib.auth import login
from django.core import signing
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from urllib.parse import urlencode
from django.http import Http404
from users.models import CustomUser
from django.urls import reverse
import string
import random

# 네이버 OAuth
NAVER_CALLBACK_URL = '/api/naver/callback/'
NAVER_STATE ='naver_login'
NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize'
NAVER_TOKEN_URL = 'https://nid.naver.com/oauth2.0/token'
NAVER_PROFILE_URL = 'https://openapi.naver.com/v1/nid/me'

# 네이버 로그인 버튼 및 로그인 성공 화면
def naver_login_page(request):
    return render(request, 'oauth_login.html')

# 네이버 인증서버로 리디렉션하는 뷰
class NaverLoginRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST', '')
        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE) # 암호화

        print('callback_url : ', callback_url)

        params = {
            'response_type': 'code',
            'client_id': settings.NAVER_CLIENT_ID,
            'redirect_uri': callback_url,
            'state': state,
        }

        return f'{NAVER_LOGIN_URL}?{urlencode(params)}'

# 네이버 로그인 완료 후 콜백 URL로 접근될 때 실행
def naver_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    # state 복호화(signing.loads)해서 확인
    if NAVER_STATE != signing.loads(state):
        raise Http404

    # 액세스 토큰 요청
    access_token = get_naver_access_token(code, state)

    # 유저 프로필 요청
    profile_response = get_naver_profile(access_token)
    print('profile request', profile_response)
    email = profile_response.get('email')
    print('email', email)

    # 유저 DB 확인 및 생성
    user = CustomUser.objects.filter(email=email).first()
    print('user', user)

    if not user:
        raw_password = generate_random_password()
        user = CustomUser(
            email=email,
            nickname=profile_response.get('nickname') or email.split('@')[0],
            name='네이버 유저',
            phone_number='000-0000-0000',
            is_active=True
        )
        user.set_password(raw_password)  # 비밀번호 해싱
        user.save()

    # 로그인
    login(request, user)

    # 로그인 성공 페이지로 리디렉션
    return redirect(f"{reverse('users_noti_api:naver_login_page')}?nickname={user.nickname}")

# 네이버 액세스 토큰 요청
def get_naver_access_token(code, state):
    params = {
        'grant_type': 'authorization_code',  # 발급
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_SECRET,
        'code': code,
        'state': state
    }

    response = requests.get(NAVER_TOKEN_URL, params=params)
    result = response.json()
    return result.get('access_token')

# 액세스 토큰을 사용해서 네이버 유저 프로필 요청
def get_naver_profile(access_token):
    # 회원정보 요청 (oauth로 받은 token과 같이 재요청)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # 회원정보 응답
    response = requests.get(NAVER_PROFILE_URL, headers=headers)

    if response.status_code != 200:
        raise Http404

    result = response.json()

    return result.get('response')

# 랜덤 비밀번호 생성
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits  # 대소문자 + 숫자
    return ''.join(random.choice(characters) for _ in range(length))

# def oauth_nickname(request):
#     access_token = request.GET.get('access_token')
#     oauth = request.GET.get('oauth')
#
#     if oauth == 'naver':
#         profile = get_naver_profile(access_token)
#     else:
#         raise Http404("지원하지 않는 OAuth 방식입니다.")
#
#     email = profile.get('email')
#     nickname = profile.get('nickname') or email.split('@')[0]
#
#     user = CustomUser.objects.filter(email=email).first()
#
#     if not user:
#         user = CustomUser.objects.create(
#             email=email,
#             nickname=nickname,
#             name='네이버 유저',
#             phone_number='000-0000-0000',
#             password='temp_password',  # 실제 서비스에서는 랜덤 비밀번호 처리 필수
#             is_active=True
#         )
#
#     login(request, user)
#
#     # 템플릿을 사용하는 경우
#     return render(request, 'oauth_login.html', {'nickname': user.nickname})