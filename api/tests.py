from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .serializers import UserProfile


class UserProfileTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('Andrew', 'andrew@google.com', 'fgvddfbdcbgbz')
        self.client.login(username='Andrew', password='fgvddfbdcbgbz')
        self.data = {'username': 'Andrew', 'first_name': 'Mike', 'last_name': 'Tyson'}

        user2 = User.objects.create(username='User2', password='876878yhh78h')
        user3 = User.objects.create(username='User3', password='876878yh45geh78h')
        user4 = User.objects.create(username='User4', password='87687var8yhh78h')

        user_profile1 = UserProfile.objects.create(user_id=1, inn="123456789011", balance=1000)
        user_profile2 = UserProfile.objects.create(user_id=2, inn="123456789012", balance=1000)
        user_profile3 = UserProfile.objects.create(user_id=3, inn="123456789013", balance=1000)
        user_profile4 = UserProfile.objects.create(user_id=4, inn="123456789014", balance=1000)

    def test_get_profile_list(self):
        response = self.client.get(reverse('profile-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_profile_detail(self):
        response = self.client.get(reverse('profile-detail', args=[self.superuser.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TransferApiValidatorTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('Andrew1', 'andrew@google.com', 'fgvddfbdcbgbz')
        self.client.login(username='Andrew1', password='fgvddfbdcbgbz')

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

    def test_validate_recipients(self):
        response = self.client.post(reverse('transfer-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
