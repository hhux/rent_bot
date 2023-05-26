from rest_framework import generics

# from rest_framework.permissions import IsAuthenticated
from .models import Moto, Yacht
from .serializers import MotoSerializer, YachtSerializer


class MotoRetrieveView(generics.ListAPIView):
    """"
    Дженерик получения всех Moto
    """
    queryset = Moto.objects.all()
    serializer_class = MotoSerializer
    # filter_backends = [DjangoFilterBackend]
    # permission_classes = [IsAuthenticated]


class YachtRetrieveView(generics.ListAPIView):
    """"
    Дженерик получения всех Yacht
    """
    queryset = Yacht.objects.all()
    serializer_class = YachtSerializer
    # filter_backends = [DjangoFilterBackend]
    # permission_classes = [IsAuthenticated]
