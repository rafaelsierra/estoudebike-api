import uuid
from django.db import models
from django.contrib.gis.db.models import PointField

from bike_auth.models import Token


class Parada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(Token, related_name='paradas')
    nome = models.CharField(max_length=100, null=True, blank=True)
    avaliacao = models.IntegerField(default=0, null=False)
    local = PointField(null=False)
    comentario = models.TextField(null=True, blank=True)
    foto = models.ImageField(upload_to='estacionamento/fotos', null=True, blank=True)
