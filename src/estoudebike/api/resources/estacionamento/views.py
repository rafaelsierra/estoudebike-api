from rest_framework import viewsets, mixins
from rest_framework.throttling import AnonRateThrottle

from api.resources.estacionamento.serializers import ParadaSerializer
from estacionamento.models import Parada


class ParadaThrottle(AnonRateThrottle):
    rate = '60/hour'
    scope = 'burst'


class ParadaView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    throttle_classes = (ParadaThrottle, )
    serializer_class = ParadaSerializer
    queryset = Parada.objects.all()
