from django.db import models
from accounts.models import CustomUser


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="wallets")
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("deposit", "Deposit"),
        ("withdraw", "Withdraw")
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="transactions")
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        wallet = Wallet.objects.get(user=self.user)

        if not self.pk:
            if self.type == "deposit":
                wallet.balance += self.amount
            elif self.type == "withdraw":
                wallet.balance -= self.amount
            wallet.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username