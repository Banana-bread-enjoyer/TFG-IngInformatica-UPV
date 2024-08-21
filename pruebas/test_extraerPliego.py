import unittest
from bs4 import BeautifulSoup
import requests
from unittest.mock import patch, MagicMock
from extraerPliego import extraer_info_pliego  # Asegúrate de importar la función desde el módulo correspondiente
from procesarTextoPDF import separar_por_secciones
from extraerSeccionesLLM import info_sections
class TestExtraerInfoPliego(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Permite que se muestren diferencias completas

    @patch('requests.get')
    @patch('extraerPliego.separar_por_secciones')
    @patch('fitz.open')
    @patch('extraerPliego.info_sections')
    def test_extraer_info_pliego_completo(self,mock_separar_por_secciones,mock_info_sections,mock_fitz_open, mock_get):
        # Simulación del HTML y PDF completo
        html = """
        <html>
            <strong>Expediente 12345</strong>
            <h2>
                <div>Construcción de un puente</div>
            </h2>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>24 meses</div>
            <span>CLASIFICACIÓN CPV</span>
            <div>45000000-7</div>
            <span>IMPORTE</span>
            <div>605,000 EUR</div>
            <span>IMPORTE (SIN IMPUESTOS)</span>
            <div>500,000 EUR</div>
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>15/12/2024</div>
            <a href="http://example.com/anexo.pdf">Anexo I.pdf</a>
        </html>
        """

        html_meta = """
        <html>
            <head>
                <meta content="url=/doc.pdf">
            </head>
        </html>
        """

        # Simulación del contenido del PDF
        mock_pdf_content = b'%PDF-1.4 ... (contenido binario del PDF)'

        # Configurando mock para las diferentes respuestas
        mock_get.side_effect = [
            MagicMock(content=html_meta.encode('utf-8')),  # HTML del meta
            MagicMock(content=mock_pdf_content)  # Contenido del PDF
        ]

        # Simulación de resultado esperado de la función
        expected_result = {
            "EXPEDIENTE": "Expediente 12345",
            "OBJETO": "Construcción de un puente",
            "LUGAR DE EJECUCIÓN": None,
            "TIPO DE CONTRATO": None,
            "TRAMITACIÓN": None,
            "IMPORTE (SIN IMPUESTOS)": "500,000 EUR",
            "IMPORTE": "605,000 EUR",
            "VALOR ESTIMADO DEL CONTRATO": None,
            "PROCEDIMIENTO": None,
            "PLAZO DE EJECUCIÓN": "24 meses",
            "CONDICIONES ESPECIALES DE EJECUCIÓN": None,
            "PLAZO DE PRESENTACIÓN": "15/12/2024",
            "CLASIFICACIÓN CPV": "45000000-7",
            'DETALLE1_ANEXO': 'Valor Detalle 1',
            'DETALLE2_ANEXO': 'Valor Detalle 2',
        }
        simulated_anexo_dict = {
            'DETALLE1_ANEXO': 'Valor Detalle 1',
            'DETALLE2_ANEXO': 'Valor Detalle 2',
        }

        # Simular el comportamiento de fitz.open
        mock_fitz_open.return_value = MagicMock()
          # Simular el valor de retorno de separar_por_secciones
       # Configurar el mock para las funciones de procesarTextoPDF
        mock_separar_por_secciones.return_value = simulated_anexo_dict
        mock_info_sections.return_value = simulated_anexo_dict
        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)
        self.assertEqual(link_anexo, "https://contrataciondelestado.es/doc.pdf")
    

    @patch('requests.get')
    def test_extraer_info_pliego_sin_anexo(self, mock_get):
        # Simulación del HTML sin un anexo
        html = """
        <html>
            <strong>Expediente 67890</strong>
            <h2>
                <div>Reparación de carretera</div>
            </h2>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>18 meses</div>
            <span>IMPORTE</span>
            <div>242,000 EUR</div>
            <span>IMPORTE (SIN IMPUESTOS)</span>
            <div>200,000 EUR</div>
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>10/11/2024</div>
        </html>
        """

        # No hay contenido de PDF porque no hay anexo
        mock_get.return_value = MagicMock(content=None)

        # Simulación de resultado esperado de la función
        expected_result = {
            "EXPEDIENTE": "Expediente 67890",
            "OBJETO": "Reparación de carretera",
            "LUGAR DE EJECUCIÓN": None,
            "TIPO DE CONTRATO": None,
            "TRAMITACIÓN": None,
            "IMPORTE (SIN IMPUESTOS)": "200,000 EUR",
            "IMPORTE": "242,000 EUR",
            "VALOR ESTIMADO DEL CONTRATO": None,
            "PROCEDIMIENTO": None,
            "PLAZO DE EJECUCIÓN": "18 meses",
            "CONDICIONES ESPECIALES DE EJECUCIÓN": None,
            "PLAZO DE PRESENTACIÓN": "10/11/2024",
            "CLASIFICACIÓN CPV": None,
        }

        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)
        self.assertIsNone(link_anexo)


    @patch('requests.get')
    def test_extraer_info_pliego_con_lotes(self, mock_get):
        # Simulación del HTML con lotes
        html = """
        <html>
            <strong>Expediente 98765</strong>
            <h2>
                <div>Construcción de edificio</div>
            </h2>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>36 meses</div>
            <span>IMPORTE</span>
            <div>1,210,000 EUR</div>
            <span>IMPORTE (SIN IMPUESTOS)</span>
            <div>1,000,000 EUR</div>
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>20/01/2025</div>
            <span>LOTES</span>
            <div>4</div>
        </html>
        """

        # Simulación de resultado esperado de la función
        expected_result = None


        result, link_anexo = extraer_info_pliego(html)
        self.assertEqual(result, expected_result)
        self.assertIsNone(link_anexo)


    @patch('requests.get')
    def test_extraer_info_pliego_html_incompleto(self, mock_get):
        # Simulación del HTML incompleto
        html = """
        <html>
            <strong>Expediente 11111</strong>
            <h2>
                <div>Construcción de parque</div>
            </h2>
            <!-- Faltan varios datos relevantes -->
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>05/10/2024</div>
        </html>
        """

        # Simulación de resultado esperado de la función
        expected_result = {
            "EXPEDIENTE": "Expediente 11111",
            "OBJETO": "Construcción de parque",
            "LUGAR DE EJECUCIÓN": None,
            "TIPO DE CONTRATO": None,
            "TRAMITACIÓN": None,
            "IMPORTE (SIN IMPUESTOS)": None,
            "IMPORTE": None,
            "VALOR ESTIMADO DEL CONTRATO": None,
            "PROCEDIMIENTO": None,
            "PLAZO DE EJECUCIÓN": None,
            "CONDICIONES ESPECIALES DE EJECUCIÓN": None,
            "PLAZO DE PRESENTACIÓN": "05/10/2024",
            "CLASIFICACIÓN CPV": None,
        }


        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)
        self.assertIsNone(link_anexo)


    @patch('requests.get')
    def test_extraer_info_pliego_anexo_fallido(self, mock_get):
        # Simulación del HTML que referencia un anexo PDF, pero el PDF no contiene información válida
        html = """
        <html>
            <strong>Expediente 54321</strong>
            <h2>
                <div>Renovación de instalaciones</div>
            </h2>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>12 meses</div>
            <span>IMPORTE</span>
            <div>363,000 EUR</div>
             <span>IMPORTE (SIN IMPUESTOS)</span>
            <div>300,000 EUR</div>
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>25/12/2024</div>
            <a href="http://example.com/anexo.pdf">Anexo I BIS</a>
        </html>
        """

        # Simulación de resultado esperado de la función
        expected_result = {
            "EXPEDIENTE": "Expediente 54321",
            "OBJETO": "Renovación de instalaciones",
            "LUGAR DE EJECUCIÓN": None,
            "TIPO DE CONTRATO": None,
            "TRAMITACIÓN": None,
            "IMPORTE (SIN IMPUESTOS)": "300,000 EUR",
            "IMPORTE": "363,000 EUR",
            "VALOR ESTIMADO DEL CONTRATO": None,
            "PROCEDIMIENTO": None,
            "PLAZO DE EJECUCIÓN": "12 meses",
            "CONDICIONES ESPECIALES DE EJECUCIÓN": None,
            "PLAZO DE PRESENTACIÓN": "25/12/2024",
            "CLASIFICACIÓN CPV": None,
        }

        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)
        self.assertEqual(link_anexo, None)

if __name__ == '__main__':
    unittest.main()
