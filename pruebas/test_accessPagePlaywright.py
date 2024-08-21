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
    def test_is_expediente_in_database(self, mock_connect):
        # Mocking the cursor and the SQL query result
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]  # Simulating that the expediente is in the database
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        expediente_name = "12345/2023"
        result = asyncio.run(is_expediente_in_database(expediente_name))
        self.assertTrue(result)

        # Test for expediente not in the database
        mock_cursor.fetchone.return_value = [0]  # Simulating that the expediente is not in the database
        result = asyncio.run(is_expediente_in_database("98765/2023"))
        self.assertFalse(result)

    @patch("playwright.async_api.Page.query_selector_all")
    async def test_collect_expedientes_from_page(self, mock_query_selector_all):
        mock_element = AsyncMock()
        mock_element.text_content.return_value = "Expediente A"
        mock_query_selector_all.return_value = [mock_element]

        page = MagicMock()
        expedientes = await collect_expedientes_from_page(page)
        self.assertEqual(len(expedientes), 1)

    @patch("playwright.async_api.async_playwright")
    @patch("pyodbc.connect")
    async def test_access_page(self, mock_connect, mock_playwright):
        # Mock database cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[None], [0]]

        # Mock Playwright browser, context, and page
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simulate expedientes on the page
        mock_page.query_selector_all.return_value = [AsyncMock(text_content=AsyncMock(return_value="Expediente A"))]
        mock_page.query_selector.return_value = None  # No more pages to paginate

        # Call the function
        expedientes_list = await access_page()
        self.assertIn("Expediente A", expedientes_list)

    @patch("playwright.async_api.async_playwright")
    async def test_get_html(self, mock_playwright):
        # Mock Playwright browser, context, and page
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simulate successful HTML retrieval
        mock_page.content.return_value = "<html></html>"
        mock_page.query_selector.return_value = None

        expediente = "Expediente A"
        html = await get_html(expediente)
        self.assertEqual(html, "<html></html>")

    @patch("playwright.async_api.async_playwright")
    @patch("pyodbc.connect")
    async def test_scrape_expedientes(self, mock_connect, mock_playwright):
        # Mock the database
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.side_effect = [[None], [0]]

        # Mock Playwright browser, context, and page
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = AsyncMock()

        mock_playwright.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Simulate expedientes and HTML content
        mock_page.query_selector_all.return_value = [AsyncMock(text_content=AsyncMock(return_value="Expediente A"))]
        mock_page.content.return_value = "<html></html>"
        mock_page.query_selector.return_value = None

        # Test scraping process
        results = await scrape_expedientes()
        self.assertEqual(results, [("Expediente A", "<html></html>")])

if __name__ == "__main__":
    unittest.main()
