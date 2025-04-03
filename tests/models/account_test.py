from decimal import Decimal
from django.db import IntegrityError
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
        no_balance_account=Account.objects.get(account_number='1')
        balace_account=Account.objects.get(account_number='3')
        self.assertEqual(no_balance_account.balance,0)
        self.assertEqual(balace_account.balance,Decimal('1200.51'))
        
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