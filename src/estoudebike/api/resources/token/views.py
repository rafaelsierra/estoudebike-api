from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from bike_auth.models import Token


class NovoAcessoBurstThrottle(AnonRateThrottle):
    rate = '100/hour'
    scope = 'burst'


class NovoAcessoDiarioThrottle(AnonRateThrottle):
    rate = '500/day'
    scope = 'daily'


class NovoAcessoView(generics.CreateAPIView):
    throttle_classes = (NovoAcessoBurstThrottle, NovoAcessoDiarioThrottle)

    def create(request, *args, **kwargs):
        token = Token.objects.create()
        return Response({'token': token.key})
