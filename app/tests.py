from django.contrib.auth.models import User
from django.test import TestCase

from app.models import UserProfile


class TransferTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('Andron', 'andron@google.com', 'fgvddfbdcbgbz')
        self.client.login(username='Andron', password='fgvddfbdcbgbz')

        user2 = User.objects.create(username='User2', password='876878yhh78h')
        user3 = User.objects.create(username='User3', password='876878yh45geh78h')
        user4 = User.objects.create(username='User4', password='87687var8yhh78h')

        user_profile1 = UserProfile.objects.create(user_id=1, inn="123456789011", balance=1000)
        user_profile2 = UserProfile.objects.create(user_id=2, inn="123456789012", balance=1000)
        user_profile3 = UserProfile.objects.create(user_id=3, inn="123456789013", balance=1000)
        user_profile4 = UserProfile.objects.create(user_id=4, inn="123456789014", balance=1000)

        self.data = {
            "payer": "123456789011",
            "transfer_amount": '20.4',
            "recipients": [
                "123456789012",
                "123456789013",
                "123456789014"
            ]
        }

    def test_payer_balance(self):
        result = UserProfile.transfer_money(**self.data)
        self.assertEqual(result, 'Перевод выполнен успешно!')

