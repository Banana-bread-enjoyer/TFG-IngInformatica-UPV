import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import pyodbc
import asyncio
from AccessPagePlaywright import (
    access_page,
    is_expediente_in_database,
    get_latest_date_from_database,
    collect_expedientes_from_page,
    scrape_expedientes,
    get_html
)

class TestAccessPagePlaywright(unittest.TestCase):

    @patch("pyodbc.connect")
    async def test_is_expediente_in_database(self, mock_connect):
        # Simula el cursor y el resultado de la consulta SQL
        mock_cursor = MagicMock()  # Simula que el expediente está en la base de datos
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        expediente_name = "CMAYOR/2020/06Y07/30"
        result = await is_expediente_in_database(expediente_name)
        self.assertTrue(result)  # Verifica que el expediente está en la base de datos

        result = await is_expediente_in_database("98765/2023")
        self.assertFalse(result)  # Verifica que el expediente no está en la base de datos

    @patch("playwright.async_api.Page.query_selector_all")
    async def test_collect_expedientes_from_page(self, mock_query_selector_all):
        # Simula el contenido de los elementos en la página
        mock_element = AsyncMock()
        mock_element.text_content.return_value = "Expediente A"
        mock_query_selector_all.return_value = [mock_element]

        page = MagicMock()
        expedientes = await collect_expedientes_from_page(page)
        self.assertEqual(len(expedientes), 1)  # Verifica que se recoja un expediente

    @patch("playwright.async_api.Page.query_selector_all")
    async def test_collect_expedientes_from_page_no_elements(self, mock_query_selector_all):
        # Simula que no hay elementos en la página
        mock_query_selector_all.return_value = []

        page = MagicMock()
        expedientes = await collect_expedientes_from_page(page)
        self.assertEqual(len(expedientes), 0)  # No se deben encontrar expedientes

    @patch("playwright.async_api.async_playwright")
    @patch("pyodbc.connect")
    async def test_access_page(self, mock_connect, mock_playwright):
        # Simula el cursor de la base de datos
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[None], [0]]

        # Simula el navegador, el contexto y la página de Playwright
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simula expedientes en la página
        mock_page.query_selector_all.return_value = [AsyncMock(text_content=AsyncMock(return_value="Expediente A"))]
        mock_page.query_selector.return_value = None  # No hay más páginas para paginar

        # Llama a la función
        expedientes_list = await access_page()
        self.assertIn("Expediente A", expedientes_list)  # Verifica que el expediente se encuentre en la lista

    @patch("playwright.async_api.async_playwright")
    async def test_get_html(self, mock_playwright):
        # Simula el navegador, el contexto y la página de Playwright
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simula la obtención exitosa del HTML
        mock_page.content.return_value = "<html></html>"
        mock_page.query_selector.return_value = None

        expediente = "Expediente A"
        html = await get_html(expediente)
        self.assertEqual(html, "<html></html>")  # Verifica que el HTML obtenido es el esperado

    @patch("playwright.async_api.async_playwright")
    @patch("pyodbc.connect")
    async def test_scrape_expedientes(self, mock_connect, mock_playwright):
        # Simula el cursor de la base de datos
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[None], [0]]

        # Simula el navegador, el contexto y la página de Playwright
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simula expedientes y contenido HTML en la página
        mock_page.query_selector_all.return_value = [AsyncMock(text_content=AsyncMock(return_value="Expediente A"))]
        mock_page.content.return_value = "<html></html>"
        mock_page.query_selector.return_value = None

        # Test del proceso de scraping
        results = await scrape_expedientes()
        self.assertEqual(results, [("Expediente A", "<html></html>")])  # Verifica que los resultados del scraping son los esperados

    @patch("pyodbc.connect")
    async def test_is_expediente_in_database_database_error(self, mock_connect):
        # Simula un error en la conexión a la base de datos
        mock_connect.side_effect = pyodbc.DatabaseError("Error de conexión")
        
        expediente_name = "CMAYOR/2020/06Y07/30"
        result = await is_expediente_in_database(expediente_name)
        self.assertFalse(result)  # Verifica el comportamiento esperado en caso de error

    @patch("playwright.async_api.Page.query_selector_all")
    async def test_collect_expedientes_from_page_multiple_elements(self, mock_query_selector_all):
        # Simula múltiples elementos en la página
        mock_element1 = AsyncMock()
        mock_element1.text_content.return_value = "Expediente A"
        mock_element2 = AsyncMock()
        mock_element2.text_content.return_value = "Expediente B"
        mock_query_selector_all.return_value = [mock_element1, mock_element2]

        page = MagicMock()
        expedientes = await collect_expedientes_from_page(page)
        self.assertEqual(len(expedientes), 2)  # Verifica que se recojan dos expedientes
        self.assertIn("Expediente A", expedientes)
        self.assertIn("Expediente B", expedientes)

    @patch("playwright.async_api.async_playwright")
    @patch("pyodbc.connect")
    async def test_access_page_multiple_pages(self, mock_connect, mock_playwright):
        # Simula múltiples páginas de expedientes
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[None], [0]]  # No hay más expedientes en la base de datos
        
        # Simula la configuración de Playwright
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simula múltiples expedientes y un botón de paginación
        mock_page.query_selector_all.return_value = [
            AsyncMock(text_content=AsyncMock(return_value="Expediente A")),
            AsyncMock(text_content=AsyncMock(return_value="Expediente B"))
        ]
        mock_page.query_selector.return_value = AsyncMock()  # Hay más páginas a paginar

        # Llama a la función
        expedientes_list = await access_page()
        self.assertIn("Expediente A", expedientes_list)
        self.assertIn("Expediente B", expedientes_list)

    @patch("playwright.async_api.async_playwright")
    async def test_get_html_page_error(self, mock_playwright):
        # Simula un error al obtener el contenido de la página
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simula un error al obtener el HTML
        mock_page.content.side_effect = Exception("Error al obtener contenido")

        expediente = "Expediente A"
        html = await get_html(expediente)
        self.assertIsNone(html)  # Verifica el comportamiento esperado en caso de error

if __name__ == "__main__":
    unittest.main()
