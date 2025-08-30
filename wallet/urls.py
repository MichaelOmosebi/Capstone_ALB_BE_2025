from django.urls import path
from .views import WalletViewSet

wallet_list = WalletViewSet.as_view({'get': 'list'})
wallet_deposit = WalletViewSet.as_view({'post': 'deposit'})
wallet_transactions = WalletViewSet.as_view({'get': 'transactions'})

urlpatterns = [
    path('', wallet_list, name='wallet-detail'),
    path('deposit/', wallet_deposit, name='wallet-deposit'),
    path('transactions/', wallet_transactions, name='wallet-transactions'),
]
