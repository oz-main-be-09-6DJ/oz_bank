from django.db import models
from utils.constants import TRANSACTION_TYPE,TRANSACTION_METHOD
from account.models import Account


class Transaction(models.Model):
    trader = models.IntegerField(null=False) # 거래자
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2, null=False) # 거래금액
    transaction_balance = models.DecimalField(max_digits=18, decimal_places=2, null=False) # 거래 후 잔액
    transaction_details = models.CharField(max_length=255, null=False, blank=True, default="")
    transaction_type = models.CharField(null=False, choices=TRANSACTION_TYPE)
    transaction_method = models.CharField(null=False, choices=TRANSACTION_METHOD)
    created_date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"{self.get_type_display()} - {self.transaction_amount}원"
