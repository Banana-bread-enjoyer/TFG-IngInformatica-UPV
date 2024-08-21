import unittest
from unittest.mock import patch, MagicMock
import fitz  # PyMuPDF
import tempfile
import ast
import pandas as pd
# Importar todas las funciones del script
from extraerTablas import (
    texto_juicio_valor,
    read_pdf,
    extract_table_info,
    extract_text,
    extraer_ofertas,
    extraer_info_acta
)


class TestPDFProcessing(unittest.TestCase):
    
    @patch("fitz.open")
    def test_read_pdf(self, mock_fitz_open):
        # Mocking the fitz Document object
        mock_doc = MagicMock()
        mock_fitz_open.return_value = mock_doc
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Texto de prueba"
        mock_doc.__iter__.return_value = [mock_page]

        text, page_count = read_pdf("dummy.pdf")

        self.assertEqual(text, " \n Texto de prueba")
        self.assertEqual(page_count, mock_doc.page_count)

    @patch("fitz.open")
    @patch("camelot.read_pdf")
    def test_extract_table_info(self, mock_camelot_read_pdf, mock_fitz_open):
        mock_pdf_document = MagicMock()
        mock_pdf_document.page_count = 15  # Número de páginas simulado
        mock_fitz_open.return_value = mock_pdf_document

        # Crear un DataFrame con valores específicos
        data = {
            "Criterios": ["Criterio Precio", "Criterio Juicio Valor", "Criterio Fórmulas"],
            "Empresa e1": [85, 90, 95],
            "Empresa e2": [75, 80, 85],
        }
        mock_df = pd.DataFrame(data)

        # Mocking the Camelot table extraction
        mock_table = MagicMock()
        mock_table.df = mock_df  # Asignando el DataFrame con datos específicos al mock de la tabla
        mock_camelot_read_pdf.return_value = [mock_table]

        # Ejecutar la función con los mocks
        result = extract_table_info(b"dummy.pdf", ["Criterio Precio", "Criterio Juicio Valor", "Criterio Fórmulas"])

        # Validar el resultado
        expected_result = {
            "Empresa e1": {"Criterio Precio": 85, "Criterio Juicio Valor": 90,  "Criterio Fórmulas": 95},
            "Empresa e2": {"Criterio Precio": 75, "Criterio Juicio Valor": 80,  "Criterio Fórmulas": 85},
        }
        self.assertEqual(result, expected_result)

    @patch("fitz.open")
    @patch("camelot.read_pdf")
    def test_extract_table_info_criterio_faltante(self, mock_camelot_read_pdf, mock_fitz_open):
        mock_pdf_document = MagicMock()
        mock_pdf_document.page_count = 15  # Número de páginas simulado
        mock_fitz_open.return_value = mock_pdf_document

        # Crear un DataFrame con valores específicos
        data = {
            "Criterios": ["Criterio Precio", "Criterio Juicio Valor", "Criterio Fórmulas"],
            "Empresa1": [85, 90, 95],
            "Empresa2": [75, 80, 85],
        }
        mock_df = pd.DataFrame(data)

        # Mocking the Camelot table extraction
        mock_table = MagicMock()
        mock_table.df = mock_df  # Asignando el DataFrame con datos específicos al mock de la tabla
        mock_camelot_read_pdf.return_value = [mock_table]

        # Ejecutar la función con los mocks
        result = extract_table_info(b"dummy.pdf", ["Criterio Precio", "Criterio Juicio Valor"])

        # Validar el resultado
        expected_result = {
            "Empresa1": {"Criterio Precio": 85, "Criterio Juicio Valor": 90},
            "Empresa2": {"Criterio Precio": 75, "Criterio Juicio Valor": 80},
        }
        self.assertEqual(result, expected_result)

    @patch("fitz.open")
    @patch("camelot.read_pdf")
    def test_extract_table_info_criterio_extra(self, mock_camelot_read_pdf, mock_fitz_open):
        mock_pdf_document = MagicMock()
        mock_pdf_document.page_count = 15  # Número de páginas simulado
        mock_fitz_open.return_value = mock_pdf_document

        # Crear un DataFrame con valores específicos
        data = {
            "Criterios": ["Criterio Precio", "Criterio Juicio Valor"],
            "Empresa e1": [85, 90],
            "Empresa e2": [75, 80],
        }
        mock_df = pd.DataFrame(data)

        # Mocking the Camelot table extraction
        mock_table = MagicMock()
        mock_table.df = mock_df  # Asignando el DataFrame con datos específicos al mock de la tabla
        mock_camelot_read_pdf.return_value = [mock_table]

        # Ejecutar la función con los mocks
        result = extract_table_info(b"dummy.pdf", ["Criterio Precio", "Criterio Juicio Valor", "Criterio Fórmulas"])

        # Validar el resultado
        expected_result = {
            "Empresa e1": {"Criterio Precio": 85, "Criterio Juicio Valor": 90,  "Criterio Fórmulas": None},
            "Empresa e2": {"Criterio Precio": 75, "Criterio Juicio Valor": 80,  "Criterio Fórmulas": None},
        }
        self.assertEqual(result, expected_result)

    @patch("tempfile.NamedTemporaryFile")
    @patch("pdfplumber.open")
    def test_extract_text(self, mock_pdfplumber_open, mock_tempfile):
        # Mocking pdfplumber
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Texto de prueba"
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdfplumber_open.return_value = mock_pdf

        # Probar la función
        mock_tempfile.return_value = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        result = extract_text(b"dummy.pdf")

        # Verificar si el resultado es un diccionario
        self.assertIsInstance(result, dict)
        self.assertIn("NÚMERO DE EMPRESAS INVITADAS", result)

    @patch("extraerTablas.extract_table_info")
    def test_extraer_ofertas(self, mock_extract_table_info):
        # Mocking the function result
        mock_extract_table_info.return_value = {"Empresa A": "1000 €"}
        
        result = extraer_ofertas([b"dummy.pdf"])
        
        # Verificar el resultado
        self.assertIsInstance(result, dict)
        self.assertIn("Empresa A", result)

    @patch("extraerTablas.extract_text")
    @patch("extraerTablas.extract_table_info")
    def test_extraer_info_acta(self, mock_extract_table_info, mock_extract_text):
        # Mocking the function results
        mock_extract_table_info.return_value = {"Empresa A": {"Criterio 1": 85}}
        mock_extract_text.return_value = {
            "NÚMERO DE EMPRESAS INVITADAS": 3,
            "NÚMERO DE LICITADORES": 3,
            "NÚMERO DE EMPRESAS SELECCIONADAS": 2,
            "NÚMERO DE EMPRESAS INCURSAS EN ANORMALIDAD": 1,
            "NÚMERO DE EMPRESAS EXCLUIDAS POR ANORMALIDAD": 1,
            "¿ES LA EMPRESA ADJUDICATARIA ANORMAL?": "No",
            "EMPRESAS EXCLUIDAS POR ANORMALIDAD": None,
        }

        result = extraer_info_acta([b"dummy.pdf"], ["Criterio 1"])

        # Verificar si el resultado es un diccionario
        self.assertIsInstance(result, dict)
        self.assertIn("VALORACIONES DE EMPRESAS", result)
        self.assertIn("NÚMERO DE EMPRESAS INVITADAS", result)


if __name__ == "__main__":
    unittest.main()
