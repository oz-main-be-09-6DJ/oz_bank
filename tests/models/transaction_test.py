from django.test import TestCase  # Django의 테스트 프레임워크
from account.models import Account
from transaction.models import Transaction
from users.models import CustomUser


class TransactionModelTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            email="transaction_test3@test.com",
            name="박유진3",
            nickname="transaction_test3",
            phone_number="01011112222",
            password="qwer1234",
        )

        account = Account.objects.create(
            account_number='11223344',
            account_type="CHECKING",
            user=user,
        )

        Transaction.objects.create(
            trader=user.id,  # CustomUser 객체 대신 id만 넘김
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

        self.assertEqual(account.account_number, '11223344')
        self.assertEqual(user.email, 'transaction_test3@test.com')

    # 여러 개의 거래 내역이 생성되는 경우
    def test_transaction_creation_multiple(self):
        user = CustomUser.objects.create(
            email="transaction_test4@test.com",
            name="박유진4",
            nickname="transaction_test4",
            phone_number="01011112223",
            password="qwer1234",
        )

        account = Account.objects.create(
            account_number='22334455',
            account_type="CHECKING",
            user=user,
        )

        Transaction.objects.create(
            trader=user.id,  # CustomUser 객체 대신 id만 넘김
            transaction_amount=10000,
            transaction_balance=20000,
            transaction_details="관리비 입금",
            account=account,
        )

        objects_count = Transaction.objects.count()
        self.assertEqual(objects_count, 2)

    # 거래 내역의 기본값이 잘 설정되는지 확인 (기본값 필드)
    def test_transaction_default_values(self):
        transaction = Transaction.objects.first()

        self.assertEqual(transaction.transaction_type, "DEPOSIT")  # 기본값 "DEPOSIT"
        self.assertEqual(transaction.transaction_method, "ATM")  # 기본값 "ATM"