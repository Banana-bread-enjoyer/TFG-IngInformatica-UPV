import asyncio
import pyodbc
from playwright.async_api import async_playwright

# Global variables
connection_string = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=ASUSMARTA\TFG;"
    r"DATABASE=TFG;"
    r"Trusted_Connection=yes;"
)
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

async def collect_expedientes_from_page(page):
    expedientes = await page.query_selector_all('a[id*="enlaceExpediente"]')
    return expedientes

async def is_expediente_in_database(expediente_name):
    cursor.execute("SELECT COUNT(1) FROM Licitaciones WHERE num_expediente = ?", (expediente_name,))
    return cursor.fetchone()[0] > 0

async def get_latest_date_from_database(cursor):
    cursor.execute("SELECT MAX(CONVERT(DATE, plazo_presentacion, 103)) FROM Licitaciones")
    result = cursor.fetchone()[0]
    if result:
        latest_year = result.year
        return f"01-01-{latest_year}"
    else:
        return "01-01-2018"

async def access_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://contrataciondelestado.es/wps/portal/licitaciones")
        await page.click('a[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:linkFormularioBusqueda"]')
        await page.fill(
            'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMinFecLimite"]',
            "01-01-2018",
        )
        await page.select_option(
            'select[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menuFormaPresentacionMAQ1_SistPresent"]',
            "Electrónica",
        )
        await page.select_option(
            'select[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:estadoLici"]',
            "Resuelta",
        )

        expedientes_list = []
        for name in ["CMAYOR/2021/06Y07/97"]:
            await page.fill(
                    'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:text71ExpMAQ"]',
                    "",
                )
            await page.fill(
                    'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:text71ExpMAQ"]',
                    name,
                )
            for tipo in ["Obras","Servicios"]:
                
                print(tipo)
                await page.select_option(
                    'select[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:combo1MAQ"]',
                    tipo,
                )
                await page.select_option(
                    'select[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menu1MAQ1"]',
                    "España",
                )
                await page.click('a[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:linkSeleccionNUTS"]')
                await page.select_option(
                    'select[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:listbox11MAQ"]',
                    "ES52 Comunitat Valenciana",
                )
                await page.click('input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:buttonAceptarSeleccionNUTS"]')
                await page.click('input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1"]')
                await page.wait_for_load_state("load")
                
                while True:
                    expedientes = await collect_expedientes_from_page(page)
                    for expediente in expedientes:
                        expediente_name = await expediente.text_content()
                        if not await is_expediente_in_database(expediente_name):
                            expedientes_list.append(expediente_name)

                    next_page_button = await page.query_selector('input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:footerSiguiente"]')
                    if next_page_button:
                        await next_page_button.click()
                        await page.wait_for_load_state("load")
                    else:
                        break
                print(expedientes_list)

        await browser.close()
        return expedientes_list

async def get_html(expediente):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://contrataciondelestado.es/wps/portal/licitaciones")
        await page.click('a[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:linkFormularioBusqueda"]')
        await page.fill(
            'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:text71ExpMAQ"]',
            expediente,
        )
        await page.click(
            'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1"]'
        )

        await page.wait_for_load_state("load")
        try:
            await page.click(f'text={expediente}')

            await page.wait_for_load_state("load")
            html = await page.content()

        except Exception as e:
            print(f"Error while fetching HTML for {expediente}: {str(e)}")
            html = None
        await browser.close()
    return html

async def scrape_expedientes():
    expedientes_list = await access_page()
    print(expedientes_list)

    html_list=[]
    for expediente in expedientes_list:
        html = await get_html(expediente)
        html_list.append(html)

    results = list(zip(expedientes_list, html_list))

    conn.close()
    return results

# To make the script executable directly, provide an entry point
if __name__ == "__main__":
    results = asyncio.run(scrape_expedientes())