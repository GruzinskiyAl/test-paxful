from rest_framework.generics import ListCreateAPIView

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionList(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
