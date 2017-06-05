from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.throttling import AnonRateThrottle

from api.resources.estacionamento.serializers import (
    BuscarEntradaSerializer,
    ParadaSerializer,
    ResultadoBuscaSerializer,
)
from estacionamento.models import Parada


class ParadaThrottle(AnonRateThrottle):
    rate = '60/hour'
    scope = 'burst'


class ParadaView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    throttle_classes = (ParadaThrottle, )
    serializer_class = ParadaSerializer
    queryset = Parada.objects.all()


class BuscarParadaPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000


class BuscarParadaView(mixins.ListModelMixin, viewsets.GenericViewSet):
    throttle_classes = (ParadaThrottle, )
    queryset = Parada.objects.all().defer('foto')
    serializer_class = ResultadoBuscaSerializer
    pagination_class = BuscarParadaPagination

    def get_queryset(self):
        serializer = BuscarEntradaSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        local = serializer['local'].value
        ponto = Point(local['lng'], local['lat'])

        resultado = self.queryset.filter(local__distance_lte=(ponto, D(m=500)))
        resultado = resultado.annotate(distancia=Distance('local', ponto))
        resultado = resultado.order_by('distancia')
        return resultado
