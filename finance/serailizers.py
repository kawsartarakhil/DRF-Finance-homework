from rest_framework import serializers
from .models import *
from accounts.serailizers import UserSerailizer
from django.core.exceptions import ValidationError


class WalletSerializer(serializers.ModelSerializer):
    user = UserSerailizer(read_only=True)
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ["balance"]


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerailizer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        wallet = Wallet.objects.get(user=instance.user)
        data["wallet"] = WalletSerializer(wallet).data
        return data