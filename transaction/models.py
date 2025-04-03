from django.db import models

from account.models import Account
from utils.constants import TRANSACTION_TYPE,TRANSACTION_METHOD


class Transaction(models.Model):
    trader = models.IntegerField(null=False) # 거래자
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2, null=False) # 거래금액
    transaction_balance = models.DecimalField(max_digits=18, decimal_places=2, null=False) # 거래 후 잔액
    transaction_details = models.CharField(max_length=255, null=False, blank=True, default="")
    transaction_type = models.CharField(null=False, choices=TRANSACTION_TYPE, default="DEPOSIT")
    transaction_method = models.CharField(null=False, choices=TRANSACTION_METHOD, default="ATM")
    created_date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')

    @property
    def transaction_type_label(self): # 입금/출금
        return self.get_transaction_type_display()

    @property
    def transaction_method_label(self): #ATM 거래/계좌이체/자동이체/카드결제/이자
        return self.get_transaction_method_display()

    def __str__(self):
        return f"{self.transaction_type_label} - {self.transaction_amount}원"



