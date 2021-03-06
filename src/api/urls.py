from django.conf.urls import url

from api.resources.token.views import NovoAcessoView
from api.resources.estacionamento.views import ParadaView, BuscarParadaView

urlpatterns = [
    url(r'^novo-acesso/$', NovoAcessoView.as_view(), name='novo-acesso'),
    url(r'^parada/$', ParadaView.as_view({'post': 'create'}), name='parada'),
    url(r'^parada/buscar/$', BuscarParadaView.as_view({'post': 'list'}), name='buscar-parada'),
]
