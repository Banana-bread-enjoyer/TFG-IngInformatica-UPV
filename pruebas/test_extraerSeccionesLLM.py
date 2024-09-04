import unittest
from unittest.mock import patch, MagicMock
from extraerSeccionesLLM import prompt, llm, extract_sections, read_pdf, info_sections
from langchain_openai import ChatOpenAI
import fitz

class TestPDFProcessing(unittest.TestCase):
    def setUp(self):
        # Sección de prueba y consultas para el modelo LLM
        self.section = "APARTADO LL\nContenido LL"
        self.query_criterios = (
            "Imprime una lista Python en formato [{'Nombre': None, "
            "'Siglas': None, 'Puntuación máxima': None, 'Puntuación mínima': None}] "
            "con los criterios principales separados por comas."
        )
        self.query_subcriterios = (
            "Imprime una lista Python en formato [{'Nombre': None, 'Puntuación máxima': None}] "
            "con todos los subcriterios dentro de 'Criterios relacionados con la calidad cuya "
            "cuantificación depende de un juicio de valor' o los apartados de la memoria que no "
            "sean sub índices como 1.1 ni sub sub índices como 1.1.1."
        )
        self.sample_text = (
            "APARTADO A\nContenido de A\nAPARTADO LL\nContenido de LL con "
            "criterios, subcriterios y más información relevante.\n"
            "APARTADO L\nContenido de L\n"
        )
        self.sample_sections = {
            "APARTADO A": "Contenido de A",
            "APARTADO LL": "Contenido de LL con criterios, subcriterios y más información relevante.",
            "APARTADO L": "Contenido de L",
        }
        # Configuración de documentos PDF simulados
        self.mock_pdf = self.create_mock_pdf()

    def create_mock_pdf(self):
        # Crea un PDF simulado con secciones específicas
        mock_pages = {
            "APARTADO LL": "APARTADO LL\nContenido de LL con criterios, subcriterios y más información relevante.",
            "APARTADO L": "APARTADO L\nContenido de L",
            "APARTADO E": "APARTADO E\nDeterminación del precio.",
            "APARTADO T": "APARTADO T\nUnidad encargada del seguimiento y ejecución.",
            "APARTADO Y": "APARTADO Y\nControl de calidad y abonos a cuenta.",
            "APARTADO U": "APARTADO U\nPlazo de recepción.",
            "APARTADO H": "APARTADO H\nRevisión de precios y subasta electrónica.",
            "APARTADO Q": "APARTADO Q\nObligación de subcontratación y tareas críticas.",
            "APARTADO W": "APARTADO W\nAbonos a cuentas.",
            "APARTADO D": "APARTADO D\nNúmero criterios.",
            "APARTADO M": "APARTADO M\nCriterios Anormales.",
        }
        return [self.create_mock_page(content) for content in mock_pages.values()]

    def create_mock_page(self, content):
        # Crea una página simulada con el contenido dado
        mock_page = MagicMock()
        mock_page.get_text.return_value = content
        return mock_page

    def test_extract_sections(self):
        # Prueba la extracción de secciones del texto
        result = extract_sections(self.sample_text)
        self.assertEqual(result, self.sample_sections)

    def test_read_pdf(self):
        # Prueba la lectura de un PDF simulado
        with patch("fitz.open", return_value=self.mock_pdf):
            text, pageLL = read_pdf(self.mock_pdf)
            # Verifica que el contenido esperado esté presente
            self.assertTrue(any(section in text for section in self.sample_sections.keys()))
            self.assertEqual(pageLL, 1)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_info_sections(self, mock_invoke):
        # Simula las respuestas del modelo LLM
        mock_invoke.side_effect = [
            MagicMock(content="Unidad encargada"),
            MagicMock(content="Sí"),
            MagicMock(content="Sí"),
            MagicMock(content="Texto de gastos por desistimiento o renuncia"),
            MagicMock(content="Sí"),
            MagicMock(content="Varios criterios"),
            MagicMock(content="Sí"),
            MagicMock(content="Sí"),
            MagicMock(content="Texto de penalidades"),
            MagicMock(content="30 días"),
            MagicMock(content="Sí"),
            MagicMock(content="No"),
            MagicMock(content="Tareas críticas: Ninguna"),
            MagicMock(content="[{'Nombre': 'Subcriterio 1', 'Puntuación máxima': 50}]"),
            MagicMock(content="[{'Nombre': 'Criterio 1', 'Siglas': 'C1', 'Puntuación máxima': 100, 'Puntuación mínima': 0}]"),
            MagicMock(content="Categoría A, Grupo B, Subgrupo C"),
            MagicMock(content="No"),
            MagicMock(content="Precio unitario"),
            MagicMock(content="No"),
        ]
        
        with patch("fitz.open", return_value=self.mock_pdf):
            result = info_sections(self.mock_pdf)

            # Verifica el contenido de las secciones
            self.assertIn("CRITERIOS DE ADJUDICACIÓN", result)
            self.assertIn("SUBCRITERIOS", result)
            self.assertIn("CLASIFICACIÓN", result)
            self.assertEqual(result["UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCION"], "Unidad encargada")
            self.assertEqual(result["CRITERIOS DE ADJUDICACION DEL PROCEDIMIENTO ABIERTO"], "Varios criterios")
            self.assertEqual(result["CONSIDERACION COMO INFRACCION GRAVE"], "Sí")
            self.assertEqual(result["GASTOS POR DESISTIMIENTO O RENUNCIA"], "Texto de gastos por desistimiento o renuncia")
            self.assertEqual(result["PLAZO DE RECEPCION"], "30 días")

            # Verifica que se han hecho el número correcto de llamadas al modelo LLM
            self.assertEqual(mock_invoke.call_count, 19)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_empty_section(self, mock_invoke):
        # Simula una sección vacía y verifica la respuesta del modelo
        self.sample_sections.pop("APARTADO LL")
        self.mock_pdf[1].get_text.return_value = "APARTADO L\nContenido de L"

        with patch("fitz.open", return_value=self.mock_pdf):
            mock_invoke.return_value = MagicMock(content="[]")
            result = info_sections(self.mock_pdf)
            # Verifica que la sección vacía sea manejada adecuadamente
            self.assertIn("CLASIFICACIÓN", result)
            self.assertEqual(result["CRITERIOS DE ADJUDICACIÓN"], [])

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_malformed_llm_response(self, mock_invoke):
        # Simula una respuesta malformada del modelo
        mock_invoke.return_value = MagicMock(content="Respuesta malformada")

        with patch("fitz.open", return_value=self.mock_pdf):
            result = info_sections(self.mock_pdf)
            # Verifica que se maneje adecuadamente una respuesta malformada
            self.assertIn("CRITERIOS DE ADJUDICACIÓN", result)
            self.assertEqual(result["CRITERIOS DE ADJUDICACIÓN"], [])

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_prompt_generation_criterios(self, mock_invoke):
        # Simula la generación de un prompt para criterios
        mock_invoke.return_value.content = (
            "[{'Nombre': 'Criterio 1', 'Siglas': 'CR1', 'Puntuación máxima': 10, 'Puntuación mínima': 5}]"
        )

        prompt_text = prompt.format(section=self.section, query=self.query_criterios)
        result = llm.invoke(prompt_text).content

        # Verifica el contenido generado en el prompt
        self.assertIn("Criterio 1", result)
        self.assertIn("Puntuación máxima", result)
        self.assertIn("Puntuación mínima", result)
        mock_invoke.assert_called_once_with(prompt_text)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_prompt_generation_subcriterios(self, mock_invoke):
        # Simula la generación de un prompt para subcriterios
        mock_invoke.return_value.content = (
            "[{'Nombre': 'Subcriterio 1', 'Puntuación máxima': 15}]"
        )

        prompt_text = prompt.format(section=self.section, query=self.query_subcriterios)
        result = llm.invoke(prompt_text).content

        # Verifica el contenido generado en el prompt
        self.assertIn("Subcriterio 1", result)
        self.assertIn("Puntuación máxima", result)
        mock_invoke.assert_called_once_with(prompt_text)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_llm_empty_response(self, mock_invoke):
        # Simula una respuesta vacía del modelo LLM
        mock_invoke.return_value.content = ""

        prompt_text = prompt.format(section=self.section, query=self.query_criterios)
        result = llm.invoke(prompt_text).content

        # Verifica que una respuesta vacía sea manejada adecuadamente
        self.assertEqual(result, "")
        mock_invoke.assert_called_once_with(prompt_text)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_llm_malformed_response(self, mock_invoke):
        # Simula una respuesta malformada del modelo LLM
        mock_invoke.return_value.content = "respuesta malformada"

        prompt_text = prompt.format(section=self.section, query=self.query_criterios)
        result = llm.invoke(prompt_text).content

        # Verifica que la respuesta malformada sea manejada adecuadamente
        self.assertEqual(result, "respuesta malformada")
        mock_invoke.assert_called_once_with(prompt_text)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_handle_multiple_invocations(self, mock_invoke):
        # Simula múltiples invocaciones al LLM y verifica que se manejen adecuadamente
        mock_invoke.side_effect = [
            MagicMock(content="[{'Nombre': 'Criterio 1', 'Puntuación máxima': 10}]"),
            MagicMock(content="[{'Nombre': 'Subcriterio 1', 'Puntuación máxima': 15}]"),
        ]

        prompt_text_criterios = prompt.format(section=self.section, query=self.query_criterios)
        result_criterios = llm.invoke(prompt_text_criterios).content
        self.assertIn("Criterio 1", result_criterios)

        prompt_text_subcriterios = prompt.format(section=self.section, query=self.query_subcriterios)
        result_subcriterios = llm.invoke(prompt_text_subcriterios).content
        self.assertIn("Subcriterio 1", result_subcriterios)

        mock_invoke.assert_any_call(prompt_text_criterios)
        mock_invoke.assert_any_call(prompt_text_subcriterios)
        self.assertEqual(mock_invoke.call_count, 2)

    @patch('langchain_openai.ChatOpenAI.invoke')
    def test_pdf_with_missing_sections(self, mock_invoke):
        # Simula un PDF donde faltan secciones esperadas y verifica el resultado
        missing_sections_pdf_content = {
            "APARTADO A": "APARTADO A\nContenido de A",
            # Nota: "APARTADO LL" y otras secciones están ausentes
        }
        mock_pdf_missing = [self.create_mock_page(content) for content in missing_sections_pdf_content.values()]

        with patch("fitz.open", return_value=mock_pdf_missing):
            result = read_pdf(mock_pdf_missing)
            # Verifica que se maneje la ausencia de secciones
            self.assertNotIn("APARTADO LL", result[0])
            self.assertEqual(result[1], None)  # Ajusta según el comportamiento esperado

if __name__ == '__main__':
    unittest.main()
