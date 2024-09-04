from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Participaciones, Valoraciones, Criterios, Empresas, Licitaciones, Cpvlicitacion
from django.contrib.auth.models import User

class StatisticsViewTest(APITestCase):
    def setUp(self):
        # Crea una licitación de prueba
        self.licitacion = Licitaciones.objects.create(num_expediente="Licitación Test")
        
        # Crea empresas de prueba
        self.empresa_1 = Empresas.objects.create(nombre_empresa="Empresa 1")
        self.empresa_2 = Empresas.objects.create(nombre_empresa="Empresa 2")
        
        # Crea participaciones de prueba
        self.participacion_1 = Participaciones.objects.create(id_licitacion=self.licitacion, id_empresa=self.empresa_1)
        self.participacion_2 = Participaciones.objects.create(id_licitacion=self.licitacion, id_empresa=self.empresa_2)
        
        # Crea criterios de prueba
        self.criterio_1 = Criterios.objects.create(nombre="Criterio 1", valor_max=10, valor_min=0)
        self.criterio_2 = Criterios.objects.create(nombre="Criterio 2", valor_max=10, valor_min=0)
        
        # Crea valoraciones de prueba
        self.valoracion_1 = Valoraciones.objects.create(id_participacion=self.participacion_1, id_criterio=self.criterio_1, puntuacion=7)
        self.valoracion_2 = Valoraciones.objects.create(id_participacion=self.participacion_2, id_criterio=self.criterio_1, puntuacion=8)
        self.valoracion_3 = Valoraciones.objects.create(id_participacion=self.participacion_1, id_criterio=self.criterio_2, puntuacion=5)
        self.valoracion_4 = Valoraciones.objects.create(id_participacion=self.participacion_2, id_criterio=self.criterio_2, puntuacion=6)
        
    def test_get_statistics_success(self):
        url = reverse('statistics-view', args=[self.licitacion.id])
        response = self.client.get(url)
        
        # Verifica el código de estado
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica que los datos en la respuesta son correctos
        data = response.json()
        self.assertEqual(len(data), 2)  # Asegúrate de que se devuelvan los criterios correctos
        self.assertEqual(data[0]['criterio'], "Criterio 1")
        self.assertEqual(data[1]['criterio'], "Criterio 2")
