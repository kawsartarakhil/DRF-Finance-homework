from django.urls import path
from .views import *


urlpatterns = [
    path("wallet/", WalletView.as_view()),
    path("transactions/", TransactionView.as_view()),
    path("transactions/<int:pk>/",TransactionDetailView.as_view()),
]