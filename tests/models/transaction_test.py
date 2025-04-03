from unittest import TestCase
from django.contrib.auth import get_user_model

from transaction.models import Transaction
from account.models import Account

User = get_user_model()

class TransactionModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="transaction_test3549522145@test.com",
            name="박유진3",
            nickname="transaction_test3549522145",
            phone_number="01169411021",
            password="qwer1234",
        )

        account = Account.objects.create(
            account_number='1699841523',
            account_type="CHECKING",
            user=user,
        )

        Transaction.objects.create(
            trader=878,
            transaction_amount=10000,
            transaction_balance=20000,
            transaction_details="관리비 입금",
            account=account,
        )

    ## 테스트
    # 생성된 인스턴스 카운트
    def test_transaction_creation(self):
        objects_count = Transaction.objects.count()

        self.assertEqual(objects_count, 1)

    # 각 필드에 잘 들어 갔는지 확인 (기본값들도 확인)
    def test_transaction_fields(self):
        transaction = Transaction.objects.first()

        self.assertEqual(transaction.transaction_amount, 10000)
        self.assertEqual(transaction.transaction_balance, 20000)
        self.assertEqual(transaction.transaction_details, "관리비 입금")
        self.assertEqual(transaction.transaction_type, "DEPOSIT")
        self.assertEqual(transaction.transaction_method, "ATM")

    # 관계 테이블 확인(계좌 및 유저 정보)
    def test_transaction_relationship(self):
        transaction = Transaction.objects.first()
        account = transaction.account
        user = account.user

        self.assertEqual(account.account_number, '1699841523')
        self.assertEqual(user.email, 'transaction_test3549522145@test.com')
