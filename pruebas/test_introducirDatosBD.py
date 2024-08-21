import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import json
import os
import pandas as pd
import pyodbc
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from unidecode import unidecode
from introducirDatosBD import *

class TestIntroducirDatosBD(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Permite que se muestren diferencias completas
        
    def test_convertNumber(self):
        self.assertEqual(convertNumber("1234,560"), 1234.56)
        self.assertEqual(convertNumber("1.234,56"), 1234.56)
        self.assertEqual(convertNumber("1234,56 €"), 1234.56)
        self.assertEqual(convertNumber("€1234,56 EUR."), 1234.56)
        self.assertEqual(convertNumber("abc"), "abc")
        self.assertEqual(convertNumber(None), None)

    def test_dict_ofertas(self):
        ofertas = {
            'item1': '1.234,56 €',
            'item2': '7890,12 EUR',
            'item3': 'Some text',
            'item4': {'PRECIO FINAL': '1000,00'}
        }
        expected = {
            'item1': 1234.56,
            'item2': 7890.12,
            'item3': 'Some text',
            'item4': 1000.00
        }
        self.assertEqual(dict_ofertas(ofertas), expected)

    def test_invert_dict(self):
        dictValores = {
            'company1': {'criterion1': 10, 'criterion2': 20},
            'company2': {'criterion1': 30}
        }
        expected = {
            'criterion1': {'company1': 10, 'company2': 30},
            'criterion2': {'company1': 20}
        }
        self.assertEqual(invert_dict(dictValores), expected)

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("flaw", "lawn"), 2)

    @patch('fuzzywuzzy.process.extract')
    def test_find_matching_company(self, mock_extract):
        mock_extract.return_value = [('company1', 90)]
        result = find_matching_company('comp1', ['company1'])
        self.assertEqual(result, 'company1')

    def test_match_list(self):
        with patch('fuzzywuzzy.process.extract') as mock_extract:
            mock_extract.return_value = [('item1', 85)]
            result = match_list('item', ['item1'])
            self.assertEqual(result, 'item1')

    @patch('fuzzywuzzy.process.extract')
    def test_unify_names(self, mock_extract):
        mock_extract.return_value = [('name1', 90)]
        dictCriterios = {'name1': {}}
        dictOferta = {'name2': {}}
        with patch('builtins.print') as mock_print:
            unify_names(dictCriterios, dictOferta)
            mock_print.assert_called_with('name2', 'name1')

    def test_find_corresponding_element(self):
        tuples_list = [('a', 'b'), ('c', 'd')]
        self.assertEqual(find_corresponding_element(tuples_list, 'a'), 'b')
        self.assertEqual(find_corresponding_element(tuples_list, 'd'), 'c')
        self.assertIsNone(find_corresponding_element(tuples_list, 'e'))

    
    def test_agrupar_empresas(self ):
        
        dictValoraciones = {'company1': {'criterio1':10, 'criterio2':10}, 'company2': {'criterio1':20, 'criterio2':20}, 'company3':{'criterio1':30, 'criterio2':30}}
        dictValSubcriterios = {'company1': {'criterio1':15, 'criterio2':15}, 'company2': {'criterio1':25, 'criterio2':25}, 'company3':{'criterio1':35, 'criterio2':35}}
        dictOfertas = {'company1': 10000, 'company2': 20000, 'company3':30000}
        dictAnormales = {}
        result = agrupar_empresas(dictValoraciones, dictValSubcriterios, dictOfertas, dictAnormales)
        expected = {'company1': {'Criterios': {'criterio1':10, 'criterio2':10}, 'Subcriterios': {'criterio1':15, 'criterio2':15}, 'Oferta': 10000, 'Expulsada': 0, 'AnormalidadEcon': 0},
                    'company2': {'Criterios': {'criterio1':20, 'criterio2':20}, 'Subcriterios': {'criterio1':25, 'criterio2':25}, 'Oferta': 20000, 'Expulsada': 0, 'AnormalidadEcon': 0},
                    'company3': {'Criterios': {'criterio1':30, 'criterio2':30}, 'Subcriterios': {'criterio1':35, 'criterio2':35}, 'Oferta': 30000, 'Expulsada': 0, 'AnormalidadEcon': 0}, }
        self.assertEqual(result, expected)

    @patch('pyodbc.connect')
    @patch('pyodbc.Cursor')
    def test_insertar_criterios(self, mock_cursor, mock_connect):
        mock_cursor.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        data = {'VALORACIONES SUBCRITERIOS': []}
        dictCriterios = [{'Nombre': 'criterion1', 'Puntuación máxima': 10, 'Siglas': 'C1'}]
        dictSubcriterios = [{'Nombre': 'subcriterion1', 'Puntuación máxima': 5}]
        
        result = insertar_criterios(dictCriterios, dictSubcriterios, data)
        self.assertIsInstance(result, dict)

    @patch('pyodbc.connect')
    @patch('pyodbc.Cursor')
    def test_insertar_empresa(self, mock_cursor, mock_connect):
        mock_cursor.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        data = {
            'nombre': 'CompanyName',
            'pyme': 'SI',
            'nif': '12345678A',
            'adjudicatario': False
        }
        
        result = insertar_empresa(data['nombre'], data['pyme'], data['nif'], data['adjudicatario'])
        self.assertIsInstance(result, int)

    @patch('pyodbc.Cursor', autospec=True)
    @patch('pyodbc.connect', autospec=True)
    def test_insertar_licitacion(self, mock_cursor, mock_conn):
        # Mock the database fetches
        mock_cursor.fetchone.side_effect = [
            None,  # First fetch: no existing licitacion
            (1,),  # Tipo procedimiento
            (2,),  # Tipo contrato
            (3,),  # Tipo tramitacion
            (100,),  # Fetch after insert, id_licitacion
            (200,),  # id_tipo_link for LinkType1
            (200,),  # id_tipo_link for LinkType2
            None,  # No existing link 1
            None,  # No existing link 2
            None,  # No existing link 3
            (300,)  # CPV id after insert
        ]

        data = {
            "EXPEDIENTE": "EXP-2024-001",
            "CLASIFICACIÓN": "Categoría 5 - Grupo A - Subgrupo 2",
            "CONDICIONES ESPECIALES DE EJECUCION A CUMPLIR": "Condiciones especiales de ejecución",
            "CONDICIONES ESPECIALES DE EJECUCIÓN": "",
            "PROCEDIMIENTO": "Procedimiento Abierto",
            "TIPO DE CONTRATO": "Contrato de Obras",
            "TRAMITACIÓN": "Urgente",
            "CRITERIOS DE ADJUDICACION": "Mejor relación calidad-precio",
            "FECHA ADJUDICACIÓN": "2024-01-15",
            "FECHA FORMALIZACIÓN": "2024-02-01",
            "FECHA ANUNCIO PERFIL DE CONTRATANTE": "2024-01-01",
            "FORMA DE PAGO": "Pago único",
            "GARANTIA DEFINITIVA": "10%",
            "GARANTIA PROVISIONAL": "5%",
            "GASTOS POR DESISTIMIENTO O RENUNCIA": "N/A",
            "IMPORTES PREVISTOS": {
                "Modificaciones": "10000",
                "Prórrogas": "5000",
                "Revisión de precios": "2000",
                "Otros Conceptos": "1000"
            },
            "INCLUSION DEL CONTROL DE CALIDAD": "Sí",
            "LUGAR DE EJECUCIÓN": "Madrid",
            "MEDIOS PARA ACREDITAR LA SOLVENCIA ECONOMICA": "Balances y cuentas anuales",
            "MEDIOS PARA ACREDITAR LA SOLVENCIA TECNICA": "Certificaciones de obras similares",
            "MEJORAS COMO CRITERIO DE ADJUDICACION": "Sí",
            "OBJETO": "Construcción de un edificio público",
            "OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION": "Sí",
            "OTROS COMPONENTES DEL VALOR ESTIMADO DEL CONTRATO": "Materiales de construcción",
            "PENALIDADES EN CASO DE INCUMPLIMIENTO DE LAS CONDICIONES": "Penalidades por día de retraso",
            "PLAZO DE EJECUCIÓN": "6 meses",
            "PLAZO DE GARANTIA": "2 años",
            "PLAZO DE PRESENTACIÓN": "15 días",
            "PLAZO DE RECEPCION": "30 días",
            "PLAZO MAXIMO DE LAS PRORROGAS": "1 año",
            "PLAZO PARA LA PRESENTACION": "2024-01-10",
            "POSIBILIDAD DE PRORROGAR EL CONTRATO": "Sí",
            "REGIMEN DE PENALIDADES": "Sí",
            "REVISION DE PRECIOS": "Aplicable",
            "SISTEMA DE PRECIOS": "Fijo",
            "SUBASTA ELECTRONICA": "No",
            "SUBCONTRATACIÓN COMO CRITERIO": "Sí",
            "TAREAS CRITICAS QUE NO PODRAN SER OBJETO DE SUBCONTRATACION": "Dirección de obra",
            "UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCION": "Departamento de Obras",
            "VALOR ESTIMADO DEL CONTRATO": "500000",
            "NÚMERO DE EMPRESAS INCURSAS EN ANORMALIDAD": 1,
            "NÚMERO DE EMPRESAS INVITADAS": 5,
            "NÚMERO DE EMPRESAS SELECCIONADAS": 3,
            "NÚMERO DE LICITADORES": 4,
            "NÚMERO DE EMPRESAS EXCLUIDAS POR ANORMALIDAD": 0,
            "PÁGINA DE INFORMACIÓN DE CRITERIOS": 9,
            "PORCENTAJE MAXIMO DE SUBCONTRATACION": "30%",
            "Links": {
                "Link a los pliegos": "http://example.com/pliegos",
                "Otros links": ["http://example.com/otro1", "http://example.com/otro2"]
            },
            "CLASIFICACIÓN CPV": "45000000-7 - Trabajos de construcción"
        }

        idAdjudicatario = 1
        
        result = insertar_licitacion(data, idAdjudicatario)

        # Verify the id_licitacion is as expected
        self.assertEqual(result, 100)

        self.assertIsInstance(result, int)

         # Check that the correct SQL insert was made
        expected_calls = [
            call.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", ('Licitaciones',)),
            call.fetchall(),
            call.execute("SELECT id_licitacion FROM Licitaciones WHERE num_expediente=?", ('EXP123',)),
            call.execute("SELECT id_procedimiento FROM TipoProcedimiento WHERE nombre_procedimiento=?", ('Procedimiento 1',)),
            call.execute("SELECT id_tipo_contrato FROM TipoContrato WHERE nombre_tipo_contrato=?", ('Tipo 1',)),
            call.execute("SELECT id_tramitacion FROM TipoTramitacion WHERE nombre_tramitacion=?", ('Tramitación 1',)),
            call.execute("INSERT INTO Licitaciones (columns...) VALUES (placeholders...)", (...)),  # Mock actual column insertion
            call.commit(),
            call.execute("SELECT id_licitacion FROM Licitaciones WHERE num_expediente=?", ('EXP123',)),
            call.fetchone(),
            call.execute("SELECT id_tipo_link FROM TipoLink WHERE texto_tipo_link=?", ('LinkType1',)),
            call.execute("SELECT id_link FROM Links WHERE link=?", ('http://link1.com',)),
            call.execute("INSERT INTO Links (link, type_link, id_licitacion) VALUES (?, ?, ?)", ('http://link1.com', 200, 100)),
            call.commit(),
            call.execute("SELECT id_link FROM Links WHERE link=?", ('http://link2.com',)),
            call.execute("INSERT INTO Links (link, type_link, id_licitacion) VALUES (?, ?, ?)", ('http://link2.com', 200, 100)),
            call.commit(),
            call.execute("SELECT id_link FROM Links WHERE link=?", ('http://link3.com',)),
            call.execute("INSERT INTO Links (link, type_link, id_licitacion) VALUES (?, ?, ?)", ('http://link3.com', 200, 100)),
            call.commit(),
            call.execute("SELECT id_cpv FROM CodigosCPV WHERE num_cpv = ?", ('12345',)),
            call.execute("INSERT INTO CodigosCPV(num_cpv, descripcion) VALUES (?, ?)", ('12345', 'Descripción CPV')),
            call.commit(),
            call.execute("SELECT id_cpv FROM CodigosCPV WHERE num_cpv = ?", ('12345',)),
            call.execute("INSERT INTO CPVLicitacion(id_licitacion, id_cpv) VALUES (?, ?)", (100, 300)),
            call.commit()
        ]
        mock_cursor.assert_has_calls(expected_calls, any_order=False)
        mock_cursor.execute.assert_called()


    @patch('pyodbc.connect')
    @patch('pyodbc.Cursor')
    def test_insertar_participacion_adjudicatario(self, mock_cursor, mock_connect):
        mock_cursor.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        data = {
            "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO": "CompanyName",
            "IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)": 1000,
            "IMPORTE TOTAL OFERTADO (CON IMPUESTOS)": 1210,
            "¿ES LA EMPRESA ADJUDICATARIA ANORMAL?": 0
        }
        idAdjudicatario = 1
        idLicitacion = 1
        dictEmpresas = {'CompanyName': {'Criterios': {}, 'Subcriterios': {}, 'Oferta': 1000}}
        idCriterios = {}

        result = insertar_participacion_adjudicatario(data, idAdjudicatario, idLicitacion, dictEmpresas, idCriterios)
        self.assertIsInstance(result, dict)

    @patch('pyodbc.connect')
    @patch('pyodbc.Cursor')
    def test_insertar_part_empresas(self, mock_cursor, mock_connect):
        mock_cursor.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        dictEmpresas = {'CompanyName': {'Criterios': {}, 'Subcriterios': {}, 'Oferta': 1000}}
        idCriterios = {}
        idLicitacion = 1
        idAdjudicatario = 1
        
        result = insertar_part_empresas(dictEmpresas, idCriterios, idLicitacion, idAdjudicatario)
        self.assertIsNone(result)  # Since `insertar_part_empresas` doesn't return anything

    @patch('pyodbc.connect')
    @patch('pyodbc.Cursor')
    def test_insertar_valoracion(self, mock_cursor, mock_connect):
        mock_cursor.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        idCriterios = {'criterion1': 1}
        idParticipacion = 1
        dictEmpresa = {'Criterios': {'criterion1': 10}}

        result = insertar_valoracion(idCriterios, idParticipacion, dictEmpresa)
        self.assertIsNone(result)  # Since `insertar_valoracion` doesn't return anything

    @patch('pyodbc.connect')
    @patch('pyodbc.Cursor')
    def test_insertar_valoracion_subcriterios(self, mock_cursor, mock_connect):
        mock_cursor.return_value = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        idSubcriterios = {'subcriterion1': 1}
        idParticipacion = 1
        dictSubcriterios = {'subcriterion1': 5}

        result = insertar_valoracion_subcriterios(idSubcriterios, idParticipacion, dictSubcriterios)
        self.assertIsNone(result)  # Since `insertar_valoracion_subcriterios` doesn't return anything

if __name__ == '__main__':
    unittest.main()
