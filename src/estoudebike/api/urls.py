from django.conf.urls import url

from api.resources.token.views import NovoAcessoView

urlpatterns = [
    url(r'^novo-acesso/$', NovoAcessoView.as_view(), name='novo-acesso'),
]
