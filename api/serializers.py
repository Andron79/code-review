from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from app.models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TransferSerializer(serializers.Serializer):

    payer = serializers.CharField()
    recipients = serializers.ListField(default=[])
    transfer_amount = serializers.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    def validate_recipients(self, value):
        recipients_list = value
        if len(recipients_list) == len(set(recipients_list)):
            for item in recipients_list:
                if not item.isdigit() or len(item) != 12:
                    msg = f'Ошибка валидации ИНН (ИНН должен быть из 12 цифр, по одному ИНН в каждой строке, ' \
                          f'без знаков препинания. Ошибка в: {item}'
                    raise serializers.ValidationError('recipients', msg)
                if not UserProfile.objects.filter(inn=item).exists():
                    msg = f'Нет такого ИНН в базе! Ошибка в: {item}'
                    raise serializers.ValidationError('recipients', msg)
        else:
            msg = f'Дубликат ИНН!'
            raise serializers.ValidationError('recipients', msg)
        return value
