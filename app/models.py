from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

from django.db.models import F


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
    def transfer_money(**kwargs):
        if Decimal(kwargs['transfer_amount']) <= UserProfile.objects.get(inn=kwargs['payer']).balance:
            transfer_sum = (round(Decimal(kwargs['transfer_amount']) / len(kwargs['recipients']), 2))
            UserProfile.objects.filter(inn=kwargs['payer']).update(balance=F('balance') - kwargs['transfer_amount'])
            UserProfile.objects.filter(inn__in=kwargs['recipients']).update(balance=F('balance') + transfer_sum)
            msg = 'Перевод выполнен успешно!'
        else:
            msg = 'Перевод не выполнен! Сумма перевода превышает остаток на счете.'
        return msg
