from decimal import Decimal
from django.test import TestCase
from account.models import Account
from users.models import CustomUser


# Create your tests here.
class AccountModelTestCase(TestCase):
    def setUp(self):
        self.user1=CustomUser.objects.create(
            email='test1@test.com',
            name='test1',
            nickname='test1',
            phone_number='300202020',
            password = '1234',
        )
        self.user2=CustomUser.objects.create(
            email='test2@test.com',
            name='test2',
            nickname='test2',
            phone_number='331231231',
            password = '12345',
        )
        #자연스러운 계좌 생성
        Account.objects.create(
            account_number = '1',
            bank_code = '001',
            account_type = 'CHECKING',
            user = self.user1,
        )
        #은행코드 입력 안한 계좌
        Account.objects.create(
            account_number = '2',
            account_type = 'CHECKING',
            user = self.user1,
        )
        #잔액 입력한 계좌
        Account.objects.create(
            account_number = '3',
            account_type = 'LOAN',
            balance = 1200.51,
            user = self.user2,
        )
        #계좌번호 중복된 계좌
        Account.objects.get_or_create(
            account_number='1',
            defaults={
                "bank_code": '001',
                "account_type": 'CHECKING',
                "balance": 1200.51,
                "user": self.user1,
            }
        )

    def test_user_accounts(self):#계좌번호 중복 체크 겸 생성된 계좌 개수 확인
        user1_account_list=Account.objects.filter(user=self.user1)
        user2_account_list=Account.objects.filter(user=self.user2)
        self.assertEqual(user1_account_list.count(),2)
        self.assertEqual(user2_account_list.count(),1)

    def test_account_balance(self):#잔액 입력 한거 안한거 비교
        no_balance_account = Account.objects.get(account_number='1')
        balance_account = Account.objects.get(account_number='3')
        self.assertEqual(no_balance_account.balance, 0)
        self.assertEqual(balance_account.balance, Decimal('1200.51'))
        
    def test_bank_code(self):#은행코드 기본값 확인 및 은행코드 이름 체크
        no_bank_code_account=Account.objects.get(account_number='2')
        bank_code_account=Account.objects.get(account_number='1')
        self.assertEqual(no_bank_code_account.bank_code,'000')
        self.assertEqual(bank_code_account.bank_code,'001')
        self.assertEqual(no_bank_code_account.bank_name,'알수없음')
        self.assertEqual(bank_code_account.bank_name,'한국은행')

    def test_account_type(self):#계좌타입 이름 체크
        checking_account=Account.objects.filter(account_type='CHECKING')
        self.assertEqual(checking_account.count(),2)
        checking_account=checking_account.first()
        loan_account=Account.objects.filter(account_type='LOAN').first()
        self.assertEqual(loan_account.account_type_name,'대출')

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from account.models import Account
from users.models import CustomUser

class AccountAPITestCase(TestCase):
    def setUp(self):
        Account.objects.all().delete()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
            name="Test User",
            nickname="Tester",
            phone_number="010-1234-5678"
        )
        self.client.force_authenticate(user=self.user)
        self.account = Account.objects.create(
            user=self.user,
            account_number="12345678",
            bank_code="001",
            account_type="CHECKING",
            balance=Decimal("10000.00")
        )
        self.create_url = reverse("account_api:list_create")
        self.detail_url = reverse("account_api:detail", kwargs={"pk": self.account.id})

    def test_create_account(self):
        data = {
            "account_number": "87654321",
            "bank_code": "002",
            "account_type": "SAVING",
            "balance": "10000.00"
        }
        response = self.client.post(self.create_url, data, format="json")

        # 디버깅 로그 추가
        print("✅ 요청 데이터:", data)
        print("✅ 서버 응답:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["balance"], "10000.00")  # 여기서 실패 발생

    def test_get_account_list(self):
        response = self.client.get(self.create_url)
        print("✅ GET 계좌 목록 응답:", response.data)  # 디버깅 로그

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)  # 응답이 dict인지 확인
        self.assertIn("results", response.data)  # "results" 키가 있는지 확인
        self.assertGreaterEqual(len(response.data["results"]), 1)  # 최소 1개 계좌 존재해야 함
        self.assertEqual(response.data["results"][0]["account_number"], self.account.account_number)

    def test_update_account_balance(self):
        data = {"balance": "20000.00"}
        response = self.client.patch(self.detail_url, data, format="json")
        print("✅ PATCH 잔액 수정 응답:", response.data)  # 디버깅 로그 추가

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["balance"], "20000.00")

    def test_delete_account(self):
        response = self.client.delete(self.detail_url)
        print("✅ DELETE 계좌 삭제 응답 코드:", response.status_code)  # 디버깅 로그 추가

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id=self.account.id).exists())

    def test_cannot_access_other_user_account(self):
        other_user = CustomUser.objects.create_user(
            email="otheruser@example.com",
            password="password123"
        )
        other_account = Account.objects.create(
            user=other_user,
            account_number="99999999",
            bank_code="003",
            account_type="LOAN",
            balance=Decimal("30000.00")
        )
        other_detail_url = reverse("account_api:detail", kwargs={"pk": other_account.id})
        response = self.client.get(other_detail_url)
        print("✅ 다른 사용자 계좌 접근 응답 코드:", response.status_code)  # 디버깅 로그 추가

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
