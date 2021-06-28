from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=15,
        unique=True,
    )
    balance = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Баланс счёта',
        default=0
    )

    class Meta:
        verbose_name = 'ИНН'
        verbose_name_plural = 'ИНН'

    def __str__(self):
        return self.inn

    @staticmethod
    def transfer_money(payer, transfer_amount, recipients):
        payer = UserProfile.objects.get(inn=payer)
        transfer_amount = Decimal(transfer_amount)
        if payer.balance >= transfer_amount:
            transfer_sum = (round(transfer_amount / len(recipients), 2))
            user_balance = payer.balance - transfer_amount
            UserProfile.objects.select_related().filter(inn=payer).update(balance=user_balance)
            for recipient in recipients:
                recipient_obj = UserProfile.objects.get(inn=recipient)
                balance = recipient_obj.balance + transfer_sum
                UserProfile.objects.select_related().filter(inn=recipient).update(balance=balance)
            msg = 'Перевод выполнен успешно!'
        else:
            msg = 'Перевод не выполнен! Сумма перевода превышает остаток на счете.'
        return msg
