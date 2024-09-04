import unittest
from bs4 import BeautifulSoup
import requests
from unittest.mock import patch, MagicMock
from extraerPliego import extraer_info_pliego
from procesarTextoPDF import separar_por_secciones
from extraerSeccionesLLM import info_sections

class TestExtraerInfoPliego(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Permite que se muestren diferencias completas en los errores

    @patch('requests.get')
    @patch('extraerPliego.separar_por_secciones')
    @patch('fitz.open')
    @patch('extraerPliego.info_sections')
    def test_extraer_info_pliego_completo(self, mock_info_sections, mock_fitz_open, mock_separar_por_secciones, mock_get):
        # Simulación del HTML completo y del contenido del PDF
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

        # Configurando el comportamiento de los mocks
        mock_get.side_effect = [
            MagicMock(content=html_meta.encode('utf-8')),  # HTML del meta
            MagicMock(content=mock_pdf_content)  # Contenido del PDF
        ]

        # Resultado esperado de la función
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

        # Configuración de mocks para funciones externas
        mock_fitz_open.return_value = MagicMock()
        mock_separar_por_secciones.return_value = simulated_anexo_dict
        mock_info_sections.return_value = simulated_anexo_dict

        # Ejecución de la función bajo prueba
        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)  # Verifica que el resultado es el esperado
        self.assertEqual(link_anexo, "https://contrataciondelestado.es/doc.pdf")  # Verifica que el enlace del anexo es el esperado

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

        # Simulación de la ausencia de contenido de PDF
        mock_get.return_value = MagicMock(content=None)

        # Resultado esperado de la función
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

        # Ejecución de la función bajo prueba
        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)  # Verifica que el resultado es el esperado
        self.assertIsNone(link_anexo)  # Verifica que no se encuentra el enlace del anexo

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

        # Simulación de la función con lotes
        expected_result = None

        # Ejecución de la función bajo prueba
        result, link_anexo = extraer_info_pliego(html)
        self.assertEqual(result, expected_result)  # Verifica que no se extrae información cuando hay lotes
        self.assertIsNone(link_anexo)  # Verifica que no se encuentra el enlace del anexo

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

        # Resultado esperado de la función
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

        # Ejecución de la función bajo prueba
        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)  # Verifica que el resultado es el esperado
        self.assertIsNone(link_anexo)  # Verifica que no se encuentra el enlace del anexo


    @patch('requests.get')
    def test_extraer_info_pliego_html_con_informacion_inesperada(self, mock_get):
        # Simulación del HTML con información inesperada
        html = """
        <html>
            <strong>Expediente 99999</strong>
            <h2>
                <div>Reparación de equipo</div>
            </h2>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>24 meses</div>
            <span>OTROS DATOS</span>
            <div>Datos adicionales no estándar</div>
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>01/01/2025</div>
        </html>
        """

        # Resultado esperado de la función
        expected_result = {
            "EXPEDIENTE": "Expediente 99999",
            "OBJETO": "Reparación de equipo",
            "LUGAR DE EJECUCIÓN": None,
            "TIPO DE CONTRATO": None,
            "TRAMITACIÓN": None,
            "IMPORTE (SIN IMPUESTOS)": None,
            "IMPORTE": None,
            "VALOR ESTIMADO DEL CONTRATO": None,
            "PROCEDIMIENTO": None,
            "PLAZO DE EJECUCIÓN": "24 meses",
            "CONDICIONES ESPECIALES DE EJECUCIÓN": None,
            "PLAZO DE PRESENTACIÓN": "01/01/2025",
            "CLASIFICACIÓN CPV": None,
        }

        # Ejecución de la función bajo prueba
        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)  # Verifica que el resultado es el esperado
        self.assertIsNone(link_anexo)  # Verifica que no se encuentra el enlace del anexo

    @patch('requests.get')
    def test_extraer_info_pliego_html_con_datos_duplicados(self, mock_get):
        # Simulación del HTML con datos duplicados
        html = """
        <html>
            <strong>Expediente 77777</strong>
            <h2>
                <div>Renovación de edificios</div>
            </h2>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>24 meses</div>
            <span>IMPORTE</span>
            <div>500,000 EUR</div>
            <span>IMPORTE (SIN IMPUESTOS)</span>
            <div>400,000 EUR</div>
            <span>IMPORTE</span> <!-- Duplicado -->
            <div>500,000 EUR</div> <!-- Duplicado -->
            <span>PLAZO DE PRESENTACIÓN</span>
            <div>30/09/2024</div>
        </html>
        """

        # Resultado esperado de la función, considerando los datos duplicados
        expected_result = {
            "EXPEDIENTE": "Expediente 77777",
            "OBJETO": "Renovación de edificios",
            "LUGAR DE EJECUCIÓN": None,
            "TIPO DE CONTRATO": None,
            "TRAMITACIÓN": None,
            "IMPORTE (SIN IMPUESTOS)": "400,000 EUR",
            "IMPORTE": "500,000 EUR",
            "VALOR ESTIMADO DEL CONTRATO": None,
            "PROCEDIMIENTO": None,
            "PLAZO DE EJECUCIÓN": "24 meses",
            "CONDICIONES ESPECIALES DE EJECUCIÓN": None,
            "PLAZO DE PRESENTACIÓN": "30/09/2024",
            "CLASIFICACIÓN CPV": None,
        }

        # Ejecución de la función bajo prueba
        result, link_anexo = extraer_info_pliego(html)
        self.assertDictEqual(result, expected_result)  # Verifica que el resultado es el esperado
        self.assertIsNone(link_anexo)  # Verifica que no se encuentra el enlace del anexo

if __name__ == '__main__':
    unittest.main()
