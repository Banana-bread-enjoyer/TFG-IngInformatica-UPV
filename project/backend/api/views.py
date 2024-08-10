from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Cpvlicitacion, Codigoscpv, Criterios, Empresas, 
    Licitaciones, Links, Participaciones, Tipocontrato,
    Tipolink, Tipoprocedimiento, Tipotramitacion, Valoraciones
)
from .serializers import (
    CpvlicitacionSerializer, CodigoscpvSerializer, CriteriosSerializer,
    EmpresasSerializer, LicitacionesSerializer,
    LinksSerializer, ParticipacionesSerializer, TipocontratoSerializer,
    TipolinkSerializer, TipoprocedimientoSerializer, TipotramitacionSerializer,
    ValoracionesSerializer
)
import numpy as np

class CpvlicitacionViewSet(viewsets.ModelViewSet):
    queryset = Cpvlicitacion.objects.all()
    serializer_class = CpvlicitacionSerializer

class CodigoscpvViewSet(viewsets.ModelViewSet):
    queryset = Codigoscpv.objects.all()
    serializer_class = CodigoscpvSerializer

class CriteriosViewSet(viewsets.ModelViewSet):
    queryset = Criterios.objects.all()
    serializer_class = CriteriosSerializer

class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializer


class LicitacionesViewSet(viewsets.ModelViewSet):
    queryset = Licitaciones.objects.all()
    serializer_class = LicitacionesSerializer

class LinksViewSet(viewsets.ModelViewSet):
    queryset = Links.objects.all()
    serializer_class = LinksSerializer

class ParticipacionesViewSet(viewsets.ModelViewSet):
    queryset = Participaciones.objects.all()
    serializer_class = ParticipacionesSerializer

class TipocontratoViewSet(viewsets.ModelViewSet):
    queryset = Tipocontrato.objects.all()
    serializer_class = TipocontratoSerializer

class TipolinkViewSet(viewsets.ModelViewSet):
    queryset = Tipolink.objects.all()
    serializer_class = TipolinkSerializer

class TipoprocedimientoViewSet(viewsets.ModelViewSet):
    queryset = Tipoprocedimiento.objects.all()
    serializer_class = TipoprocedimientoSerializer

class TipotramitacionViewSet(viewsets.ModelViewSet):
    queryset = Tipotramitacion.objects.all()
    serializer_class = TipotramitacionSerializer

class ValoracionesViewSet(viewsets.ModelViewSet):
    queryset = Valoraciones.objects.all()
    serializer_class = ValoracionesSerializer

class StatisticsView(APIView):
    def get(self, request, licitacion_id):
        try:
            # Get all participaciones related to this licitacion
            participaciones = Participaciones.objects.filter(id_licitacion=licitacion_id)
            
            # Get all valoraciones related to these participaciones
            valoraciones = Valoraciones.objects.filter(id_participacion__in=participaciones)
            # Get unique criterios for which we have valoraciones
            criterios = Criterios.objects.filter(id_criterio__in=valoraciones.values_list('id_criterio', flat=True)).distinct()
            criteriosSumar = Criterios.objects.filter(
                id_criterio__in=valoraciones.values_list('id_criterio', flat=True),
                id_padre__isnull=True
            ).distinct()
            statistics = []
            empresas_total_points = {}
            for participacion in participaciones:
                empresa_id = participacion.id_empresa.id_empresa  # Assuming Participaciones has a foreign key to Empresa
                total_points = 0
                for criterio in criteriosSumar:
                    valoracion = valoraciones.filter(
                        id_participacion=participacion,
                        id_criterio=criterio
                    ).first()
                    if valoracion and valoracion.puntuacion is not None:
                        total_points += valoracion.puntuacion
                
                if empresa_id in empresas_total_points:
                    empresas_total_points[empresa_id] += total_points
                else:
                    empresas_total_points[empresa_id] = total_points

            # Determine the first and second highest total points
            sorted_empresas = sorted(empresas_total_points.items(), key=lambda item: item[1], reverse=True)
            top_empresas = sorted_empresas[:2] if sorted_empresas else []
            if len(top_empresas) == 2:
                top_empresa_1_id = top_empresas[0][0]
                top_empresa_2_id = top_empresas[1][0]
            for criterio in criterios:
                diferencia=""
                if len(top_empresas) == 2:
                    puntuacion_1 = valoraciones.filter(
                            id_participacion__id_empresa=top_empresa_1_id,
                            id_participacion__id_licitacion=licitacion_id,
                            id_criterio=criterio
                        ).first()
                    if puntuacion_1:
                        puntuacion_1=puntuacion_1.puntuacion
                    puntuacion_2 = valoraciones.filter(
                            id_participacion__id_empresa=top_empresa_2_id,
                            id_participacion__id_licitacion=licitacion_id,
                            id_criterio=criterio
                        ).first()
                    if puntuacion_2:
                        puntuacion_2=puntuacion_2.puntuacion
                    if puntuacion_1 and puntuacion_2:
                        diferencia=puntuacion_1-puntuacion_2
                        diferencia=round(diferencia,2)

                # Get puntuaciones for the current criterio
                puntuaciones = valoraciones.filter(id_criterio=criterio).values_list('puntuacion', flat=True)
                puntuaciones = list(puntuaciones)
                median = average = standard_deviation = valor_max=valor_min=0
                if puntuaciones:
                    puntuaciones=[value for value in puntuaciones if value!=None]
                    if puntuaciones!=[]:
                        median = np.median(puntuaciones)
                        average = np.mean(puntuaciones)
                        standard_deviation = np.std(puntuaciones)
                        valor_max = max(puntuaciones)
                        valor_min = min(puntuaciones)
                    
                median = round(median, 2)
                average = round(average, 2)
                standard_deviation = round(standard_deviation, 2)
                statistics.append({
                    'criterio': criterio.nombre,
                    'peso':criterio.valor_max,
                    'inaceptable':criterio.valor_min,
                    'max':valor_max,
                    'min':valor_min,
                    'median': median,
                    'average': average,
                    'standard_deviation': standard_deviation,
                    'id':criterio.id_criterio,
                    'diferencia':diferencia
                })
            

                
                    

            return Response(statistics, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Log the error for debugging purposes
            import logging
            logging.error(f"An error occurred: {str(e)}")
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)