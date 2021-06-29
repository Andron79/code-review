from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import TransferSerializer, UserProfileSerializer
from app.models import UserProfile


class UserProfileSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class TransferViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TransferSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pay_status = UserProfile.transfer_money(**serializer.data)
        return Response(pay_status)
