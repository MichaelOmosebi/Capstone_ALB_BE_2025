from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, DepositSerializer

class WalletViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_wallet(self, user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet

    def list(self, request):
        """
        GET /api/wallets/ -> returns wallet summary (balance + recent transactions)
        """
        wallet = self.get_wallet(request.user)
        serializer = WalletSerializer(wallet, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='deposit')
    def deposit(self, request):
        """
        POST /api/wallets/deposit/  body: { "amount": "100.00" }
        Credits the authenticated user's wallet.
        """
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        wallet = self.get_wallet(request.user)
        with transaction.atomic():
            wallet.credit(amount, description="Manual deposit via API")

        return Response({"detail": f"Deposited {amount}", "balance": wallet.balance}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='transactions')
    def transactions(self, request):
        """
        GET /api/wallets/transactions/ -> list of transactions for the authenticated user
        """
        wallet = self.get_wallet(request.user)
        qs = wallet.transactions.all()
        serializer = TransactionSerializer(qs, many=True)
        return Response(serializer.data)
