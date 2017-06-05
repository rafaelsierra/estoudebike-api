from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from bike_auth.models import Token


class NovoAcessoThrottle(AnonRateThrottle):
    rate = '100/hour'
    scope = 'burst'


class NovoAcessoView(generics.CreateAPIView):
    throttle_classes = (NovoAcessoThrottle, )

    def create(request, *args, **kwargs):
        token = Token.objects.create()
        return Response({'token': token.key})
