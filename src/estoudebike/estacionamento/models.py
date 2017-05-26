import uuid

from django.contrib.gis.db.models import PointField, GeoManager
from django.db import models

from bike_auth.models import Token


class Parada(models.Model):
    objects = GeoManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(Token, related_name='paradas')
    nome = models.CharField(max_length=100, null=True, blank=True)
    avaliacao = models.IntegerField(default=0, null=False)
    local = PointField(null=False)
    comentario = models.TextField(null=True, blank=True)
    foto = models.TextField(null=True, blank=True)
