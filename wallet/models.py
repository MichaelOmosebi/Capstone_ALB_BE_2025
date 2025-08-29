from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def credit(self, amount, description: str | None = None):
        """
        Credit the wallet and log a transaction.
        amount may be Decimal, str or number.
        """
        amount = Decimal(str(amount))
        self.balance = (self.balance or Decimal('0.00')) + amount
        self.save(update_fields=['balance', 'updated_at'])
        Transaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=Transaction.CREDIT,
            description=description or "Credit"
        )

    def debit(self, amount, description: str | None = None):
        """
        Debit the wallet and log a transaction. Raises ValueError if insufficient funds.
        """
        amount = Decimal(str(amount))
        if (self.balance or Decimal('0.00')) < amount:
            raise ValueError("Insufficient wallet balance")
        self.balance = (self.balance or Decimal('0.00')) - amount
        self.save(update_fields=['balance', 'updated_at'])
        Transaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=Transaction.DEBIT,
            description=description or "Debit"
        )

    def __str__(self):
        return f"{self.user} wallet: {self.balance}"


class Transaction(models.Model):
    CREDIT = 'CREDIT'
    DEBIT = 'DEBIT'
    TRANSACTION_CHOICES = (
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} {self.amount} ({self.wallet.user})"
