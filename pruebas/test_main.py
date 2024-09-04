import unittest
from unittest.mock import patch, Mock
import requests
from bs4 import BeautifulSoup
import asyncio
import json
from io import StringIO

# Importar todas las funciones que vamos a testear
from main import (
    get_names,
    open_link,
    docs_valoraciones,
    docs_juicio_valor,
    fechas_anuncio_form,
    acceder_seccion,
    get_link_licitacion,
    main,
    save_dict_to_json,
    links
)

class TestExpedientes(unittest.TestCase):

    def test_get_names_sin_siglas(self):
        criterios = [
            {"Nombre": "Criterio 1", "Siglas": "C1"},
            {"Nombre": "Criterio 2", "Siglas": "C2"}
        ]
        nombres = get_names(criterios, sub=False)
        self.assertEqual(nombres, ["Criterio 1 (C1)", "Criterio 2 (C2)"])

    def test_get_names_con_siglas(self):
        criterios = [
            {"Nombre": "Criterio 1", "Siglas": None},
            {"Nombre": "Criterio 2", "Siglas": "C2"}
        ]
        nombres = get_names(criterios, sub=False)
        self.assertEqual(nombres, ["Criterio 1", "Criterio 2 (C2)"])

    @patch("main.requests.get")
    def test_open_link(self, mock_get):
        # Simulación de una respuesta
        mock_response = Mock()
        mock_response.content = b'<meta content="url=/fake_link">'
        mock_get.return_value = mock_response

        # Llamada a la función
        data, link = open_link({"href": "http://example.com"})
        self.assertIn("https://contrataciondelestado.es", link)
        self.assertIsInstance(data, bytes)

    @patch("main.open_link")
    def test_docs_valoraciones(self, mock_open_link):
        mock_open_link.return_value = (b'Data', "http://example.com/doc.pdf")
        html = '<html><table id="viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux"><td><span>ACTA ADJUDICACIÓN</span></td><td><a href="valoraciones.es"></td></table></html>'
        documentos = docs_valoraciones(html)
        self.assertEqual(len(documentos), 1)

    @patch("main.open_link")
    def test_docs_juicio_valor(self, mock_open_link):
        mock_open_link.return_value = (b'Data', "http://example.com/doc.pdf")
        html = '<html><table id="viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux"><td><span>JUICIO DE VALOR</span></td><td><a href="juiciovalor.es"></td></table></html>'
        documentos = docs_juicio_valor(html)
        self.assertEqual(len(documentos), 1)

    @patch("main.acceder_seccion")
    @patch("main.extraer_fecha")
    def test_fechas_anuncio_form(self, mock_extraer_fecha, mock_acceder_seccion):
        mock_acceder_seccion.return_value = '<html></html>'
        mock_extraer_fecha.return_value = "2023-01-01"
        html = '<html></html>'
        dictFechas = fechas_anuncio_form(html)
        self.assertEqual(dictFechas["FECHA ANUNCIO PERFIL DE CONTRATANTE"], "2023-01-01")
        self.assertEqual(dictFechas["FECHA FORMALIZACIÓN"], "2023-01-01")

    @patch("main.requests.get")
    def test_acceder_seccion(self, mock_get):
        # Simular respuestas para la función open_link
        mock_response = Mock()
        mock_response.content = b'<meta content="url=/fake_link">'
        mock_get.return_value = mock_response

        # Ejecutar la función con un html simulado
        html = '<html><td><div>Pliego</div></td><td><div><a href="pliego.es"></div></td></html>'
        data = acceder_seccion(html, "Pliego")
        self.assertIsNotNone(data)
        self.assertEqual(links["Pliego"], "https://contrataciondelestado.es/fake_link")

    def test_save_dict_to_json(self):
        data = {"key": "value"}
        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            save_dict_to_json(data, "dummy.json")
            mock_file.assert_called_once_with("dummy.json", "w", encoding="utf-8")

if __name__ == "__main__":
    unittest.main()
