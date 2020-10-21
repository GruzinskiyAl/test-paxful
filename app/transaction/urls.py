from django.urls import path
from transaction.views import TransactionList

urlpatterns = [
    path('', TransactionList.as_view(), name='list'),
]
