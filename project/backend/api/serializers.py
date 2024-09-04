from rest_framework import serializers
from .models import Cpvlicitacion, Codigoscpv, Criterios, Empresas, Licitaciones, Links, Participaciones, Tipocontrato, Tipolink, Tipoprocedimiento, Tipotramitacion, UpdateDate, Valoraciones


class UpdateDateSerializer(serializers.ModelSerializer):
    last_update = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S', input_formats=['%d/%m/%Y, %H:%M:%S'])
    class Meta:
        model = UpdateDate
        fields = ['last_update']



class CodigoscpvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codigoscpv
        fields = '__all__'


class CriteriosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Criterios
        fields = '__all__'


class EmpresasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = '__all__'

class TipoprocedimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoprocedimiento
        fields = '__all__'

class TipocontratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipocontrato
        fields = '__all__'


class TipotramitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipotramitacion
        fields = '__all__'

class LicitacionesSerializer(serializers.ModelSerializer):
    procedimiento = TipoprocedimientoSerializer(read_only=True)
    tramitacion = TipotramitacionSerializer(read_only=True)
    tipo_contrato = TipocontratoSerializer(read_only=True)
    adjudicatario= EmpresasSerializer(read_only=True)
    class Meta:
        model = Licitaciones
        fields = '__all__'

class CpvlicitacionSerializer(serializers.ModelSerializer):
    id_cpv = CodigoscpvSerializer(read_only=True)
    class Meta:
        model = Cpvlicitacion
        fields = '__all__'


class TipolinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipolink
        fields = '__all__'

class LinksSerializer(serializers.ModelSerializer):
    type_link=TipolinkSerializer(read_only=True)
    class Meta:
        model = Links
        fields = '__all__'


class ParticipacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participaciones
        fields = '__all__'

class ValoracionesSerializer(serializers.ModelSerializer):
    id_criterio=CriteriosSerializer(read_only=True)
    class Meta:
        model = Valoraciones
        fields = '__all__'
