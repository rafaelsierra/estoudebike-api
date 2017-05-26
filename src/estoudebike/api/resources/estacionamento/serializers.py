import base64
import io
from PIL import Image

from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from estacionamento.models import Parada


class PointFieldAPI(serializers.Field):
    def to_representation(self, obj):
        return {'lat': obj.y, 'lng': obj.x}

    def to_internal_value(self, data):
        return Point(data['lng'], data['lat'])


class ParadaSerializer(serializers.ModelSerializer):
    comentario = serializers.CharField(required=False)
    foto = serializers.CharField(required=False)
    local = PointFieldAPI()

    class Meta:
        model = Parada
        read_only_fields = ('id',)
        fields = (
            'id',
            'token',
            'nome',
            'avaliacao',
            'local',
            'comentario',
            'foto'
        )

    def validate_local(self, local):
        if not -180 <= local.x <= 180 or not -90 <= local.y <= 90:
            raise serializers.ValidationError(_('Local especificado inválido'))
        return local

    def validate_avaliacao(self, avaliacao):
        if not 0 <= avaliacao <= 5:
            raise serializers.ValidationError(_('Avaliação inválida'))
        return avaliacao

    def validate_foto(self, foto):
        if len(foto) > 0:
            # Remove a informacao que a foto é base64
            if 'base64' in foto[:30]:
                try:
                    foto = foto.split('base64,')[1]
                except IndexError:
                    raise serializers.ValidationError(_('Foto corrompida'))

            try:
                im = Image.open(io.BytesIO(base64.b64decode(foto)))
            except (OSError, ValueError):
                raise serializers.ValidationError(_('Foto corrompida'))
            else:
                if im.size[1] > im.size[0]:
                    # Gira a imagem pra ter uma logica de crop so
                    rotacionada = True
                    im = im.rotate(90)
                else:
                    rotacionada = False

                # Cropa a imagem pra ser um quadrado
                x1 = (im.size[0] / 2) - (im.size[1] / 2)
                x2 = (im.size[0] / 2) + (im.size[1] / 2)
                im = im.crop((x1, 0, x2, im.size[1]))

                # Redimensiona a foto se precisar e salva com apenas 85% de qualidade
                if im.size[0] > 1000:
                    im.thumbnail((1000, 1000))

                # Rotaciona a imagem de volta
                if rotacionada:
                    im = im.rotate(-90)
                nova_im = io.BytesIO()
                im.save(nova_im, 'JPEG', quality=85)
                foto = nova_im
        return foto
