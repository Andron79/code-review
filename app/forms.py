from django import forms
from .models import UserProfile


class TransferForm(forms.Form):
    payer = forms.ModelChoiceField(
        queryset=UserProfile.objects.all(),
        empty_label='ИНН плательщика',
        label='Плательщик'
    )
    recipients = forms.CharField(
        widget=forms.Textarea,
        label='ИНН',

    )
    transfer_amount = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        label='Сумма списания:'
    )

    def clean_recipients(self):
        recipients = self.cleaned_data['recipients']
        payer = self.cleaned_data['payer']
        recipients_list = list(recipients.split())
        if len(recipients_list) == len(set(recipients_list)):
            for item in recipients_list:
                if not item.isdigit() or len(item) != 12:
                    msg = f'Ошибка валидации ИНН (ИНН должен быть из 12 цифр, по одному ИНН в каждой строке, ' \
                          f'без знаков препинания. Ошибка в: {item}'
                    self.add_error('recipients', msg)
                if not UserProfile.objects.filter(inn=item).exists():
                    msg = f'Нет такого ИНН в базе! Ошибка в: {item}'
                    self.add_error('recipients', msg)
                if str(payer) == item:
                    msg = f'Самому себе нельзя переводить. Ошибка в: {item}'
                    self.add_error('recipients', msg)
        else:
            msg = f'Дубликат ИНН!'
            self.add_error('recipients', msg)

        return recipients_list
