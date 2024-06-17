import asyncio
from playwright.async_api import async_playwright


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


async def access_page(expediente):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the webpage
        await page.goto("https://contrataciondelestado.es/wps/portal/licitaciones")
        await page.click(
            'a[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:linkFormularioBusqueda"]'
        )

        # Fill out and submit the form
        await page.fill(
            'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:text71ExpMAQ"]',
            expediente,
        )
        await page.select_option(
            'select[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menuFormaPresentacionMAQ1_SistPresent"]',
            "Electrónica",
        )
        await page.click(
            'input[id="viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1"]'
        )

        await page.wait_for_load_state("load")
        try:

            await page.get_by_text(expediente).click()

            await page.wait_for_load_state("load")
            # Extract the HTML from the resulting page

            html = await page.content()

            # Close the browser
            await browser.close()
        except:
            html = None

        return html
