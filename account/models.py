from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from utils.constants import BANK_CODES, ACCOUNT_TYPE

User = get_user_model()


class Account(models.Model):
    account_number = models.CharField('Account Number', max_length=20, unique=True)
    bank_code = models.CharField('Bank Code', max_length=10, choices=BANK_CODES, default='000')
    account_type = models.CharField('Account Type', max_length=20, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    deleted_at = models.DateTimeField(verbose_name='Deleted Date', null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name='Updated Date', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def bank_name(self):
        return self.get_bank_code_display()
    
    @property
    def account_type_name(self):
        return self.get_account_type_display()

    def __str__(self):
        return f'[{self.get_account_type_display()}]{self.account_number}({self.get_bank_code_display()})'