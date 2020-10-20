from django.urls import path
from transaction.views import TransactionList

urlpatterns = [
    path('list/', TransactionList.as_view(), name='list'),
]
