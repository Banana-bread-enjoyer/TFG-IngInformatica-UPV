import asyncio
import json
from AccessPagePlaywright import access_page
from bs4 import BeautifulSoup
import requests
from extraerPliego import extraer_info_pliego
from extraerAdjudicacion import extraer_info_adjudicacion, extraer_fecha
from extraerTablas import (
    extract_table_info,
    extract_text,
    texto_juicio_valor,
    extraer_info_acta,
    # extract_importes,
)
import csv
import os


# mongo = "mongodb+srv://martaramalho:tfg_etsinf@licitacionessectorpubli.veo3b98.mongodb.net/?retryWrites=true&w=majority&appName=LicitacionesSectorPublico"
links = {
    "Licitación": "",
    "Anuncio de Licitación": "",
    "Pliego": "",
    "Anexo I": "",
    "Adjudicación": "",
    "Formalización": "",
    "Actas de adjudicación": [],
    "Actas de valoración de criterios mediante juicio de valor": [],
}


def get_names(criterios, sub):
    nombres = []
    for item in criterios:
        if not sub:
            if item["Siglas"]:
                nombres.append(item["Nombre"] + " (" + item["Siglas"] + ")")
            else:
                nombres.append(item["Nombre"])
        else:
            nombres.append(item["Nombre"])
    """ if not sub:
        nombres.append("PUNTUACIÓN TOTAL") """
    return nombres


def open_link(a_html):
    response = requests.get(a_html.get("href"))
    html_pdf = response.content
    soup_pdf = BeautifulSoup(html_pdf, "html.parser")
    link = soup_pdf.find("meta")
    link = "https://contrataciondelestado.es" + link.get("content").split("url=")[
        1
    ].strip("'")
    data = requests.get(link)
    data = data.content
    return data, link


def docs_valoraciones(html):
    soup = BeautifulSoup(html, "html.parser")
    nombres = [
        "ÓRGANO ASISTENCIA",
        "PROPUESTA ADJUDICACIÓN",
        "ACTA ADJUDICACIÓN",
        "ACTA AUTOMÁTICAMENTE",
        "APROBACIÓN EXPEDIENTE",
        "APERTURA OFERTAS",
        "INFORME CRITERIOS",
    ]
    documentos = []
    table = soup.find(id="viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux")
    spans = table.find_all("span")
    for span in spans:
        for nombre in nombres:
            # SE HA CAMBIADO
            if (
                all(word in span.text.upper() for word in nombre.split())
                and not "rectificación" in nombre.lower()
            ):
                a = span.find_parent().find_next_sibling().find("a")
                data, link = open_link(a)
                links["Actas de adjudicación"].append(link)
                documentos.append(data)
                break
    documentos.reverse()
    return documentos


def docs_juicio_valor(html):
    nombre = "JUICIO DE VALOR"

    soup = BeautifulSoup(html, "html.parser")
    documentos = []
    table = soup.find(id="viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux")
    spans = table.find_all("span")
    for span in spans:
        if (
            nombre in span.text.upper()
            or "oferta técnica" in span.text
            or "cuantificables automáticamente" in span.text
        ):
            a = span.find_parent().find_next_sibling().find("a")
            data, link = open_link(a)
            links["Actas de valoración de criterios mediante juicio de valor"].append(
                link
            )
            documentos.append(data)
    documentos.reverse()
    return documentos


def fechas_anuncio_form(html):
    dictFechas = {}
    anuncio = acceder_seccion(html, "Anuncio de Licitación")
    soupAnuncio = BeautifulSoup(anuncio, "html.parser")
    dictFechas["FECHA ANUNCIO PERFIL DE CONTRATANTE"] = extraer_fecha(soupAnuncio)
    try:
        formalizacion = acceder_seccion(html, "Formalización")
        soupForm = BeautifulSoup(formalizacion, "html.parser")
        dictFechas["FECHA FORMALIZACIÓN"] = extraer_fecha(soupForm)
    except:
        dictFechas["FECHA FORMALIZACIÓN"] = None
    return dictFechas


def acceder_seccion(html, sec):
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div")
    pliego = None
    for div in divs:
        if div.text == "Rectificación de " + sec:
            pliego = div
            break
        elif not pliego and div.text == sec:
            pliego = div
            break
    try:
        a_html = pliego.find_parent().find_next_sibling().find("a")
        data, link = open_link(a_html)
        links[sec] = link
    except:
        links[sec] = None
        return None
    return data


def get_link_licitacion(html):
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find(id="fila18")
    li = ul.find("li")
    li = li.find_next_sibling()
    a = li.find("a")
    link = a.get("href")
    return link


async def main(expediente):
    # expediente = "CMAYOR/2018/01Y30/54"
    html = await access_page(expediente)
    if html == None:
        print("No está")
        return
    links["Licitación"] = get_link_licitacion(html)
    val = docs_valoraciones(html)
    pliego = acceder_seccion(html, "Pliego")
    infoPliego, linkAnexo = extraer_info_pliego(pliego)
    if infoPliego == None:
        return None
    links["Anexo I"] = linkAnexo
    if infoPliego["CRITERIOS DE ADJUDICACIÓN"]:
        nombresCriterios = get_names(infoPliego["CRITERIOS DE ADJUDICACIÓN"], False)
        # print(nombresCriterios)
        infoActa = extraer_info_acta(val, nombresCriterios)
    else:
        infoActa = None
    adj = acceder_seccion(html, "Adjudicación")
    infoAdj = extraer_info_adjudicacion(adj)
    # print(infoAdj)
    fechas = fechas_anuncio_form(html)
    # print(fechas)
    # nombresSubcriterios = get_names(ejemploSubcriterios)
    docsJuicioValor = docs_juicio_valor(html)
    if infoPliego["SUBCRITERIOS"] and len(docsJuicioValor) > 0:
        nombresSubcriterios = get_names(infoPliego["SUBCRITERIOS"], True)
        # print(nombresSubcriterios)
        valoracionesSub = texto_juicio_valor(docsJuicioValor, nombresSubcriterios)
    else:
        valoracionesSub = None
    # print("--------------------------------------")
    myDict = {
        **infoPliego,
        **infoAdj,
        **fechas,
        "Links": links,
        "VALORACIONES SUBCRITERIOS": valoracionesSub,
    }
    if infoActa:
        myDict = {**infoActa, **myDict}
    # print(myDict)
    save_dict_to_json(
        myDict, "../JSONExpedientes/" + expediente.replace("/", "_") + ".json"
    )
    links["Actas de adjudicación"] = []
    links["Actas de valoración de criterios mediante juicio de valor"] = []


def save_dict_to_json(data, file_path):
    """
    Saves a dictionary to a JSON file.

    Parameters:
    data (dict): The dictionary to save.
    file_path (str): The path to the file where the JSON will be saved.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(
                data,
                json_file,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )
        print(f"Dictionary successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the dictionary to JSON: {e}")


def export_dict_to_csv(data, filename):
    # Obtener las claves del diccionario como cabeceras de columnas

    for key, value in data.items():
        if not isinstance(value, list):
            data[key] = [value]

    headers = data.keys()

    # Abrir el archivo en modo escritura
    with open(filename, "w", newline="") as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Escribir las cabeceras
        writer.writeheader()

        # Escribir los datos
        # Asumimos que todas las listas en el diccionario tienen la misma longitud
        rows = zip(*data.values())
        for row in rows:
            writer.writerow(dict(zip(headers, row)))


async def missing_data(data):
    # expediente = "CMAYOR/2018/01Y30/54"
    newData = data
    expediente = data["EXPEDIENTE"]
    html = await access_page(expediente)
    if html == None:
        print("No está")
        return
    docs_valoraciones(html)
    docs_juicio_valor(html)
    print(links["Actas de adjudicación"])
    print(links["Actas de valoración de criterios mediante juicio de valor"])
    newData["Links"]["Actas de adjudicación"] = links["Actas de adjudicación"]
    newData["Links"]["Actas de valoración de criterios mediante juicio de valor"] = (
        links["Actas de valoración de criterios mediante juicio de valor"]
    )
    linksLoop = newData["Links"]["Actas de adjudicación"]
    linksLoop.reverse()
    linksLoop = (
        linksLoop
        + newData["Links"]["Actas de valoración de criterios mediante juicio de valor"]
    )

    val = []
    for link in linksLoop:
        dataLinks = requests.get(link)
        dataLinks = dataLinks.content
        val.append(dataLinks)
    importes = extract_importes(val)
    newData["OFERTA ECONÓMICA"] = importes
    print(importes)
    return newData


# Running the async main function
if __name__ == "__main__":
    expedientes = [
        "CMAYOR/2021/07Y10/72"
        # "CMAYOR/2018/30/34"
        # "CMAYOR/2018/30/36"
        # "CMAYOR/2020/03Y05/32",
        # "CMAYOR/2020/06Y07/152",
        # "CMAYOR/2020/06Y15/141",
        # "CMAYOR/2020/06Y15/156",
        # "CMAYOR/2021/03Y03/122",
        # "CMAYOR/2021/06Y03/230",
        # "CMAYOR/2021/06Y07/356",
        # "CMAYOR/2021/06Y07/97",
        # "CMAYOR/2021/07Y10/113",
        # "CMAYOR/2022/08Y09/114",
        # "CMAYOR/2022/08Y09/34",
        # "CNMY18/03-3/24",
        # "CNMY18/03-3/46",
        # "CNMY18/06-6/43",
        # "CNMY18/06-6/9",
        # "CNMY18/18-18/10",
        # "CNMY18/18-18/7",
        # "CNMY18/18-18/8",
        # "CNMY18/AT00A/006",
        # "CNMY18/AT00A/108",
        # "CNMY18/AT00A/74",
        # "CNMY18/AT00A/80",
        # "CNMY18/AT00A/81",
        # "CNMY18/AT00A/82",
        # "CNMY18/AT00A/95",
        # "CNMY18/AT00A/96",
        # "CNMY18/CS00D/18",
        # "CNMY18/CS30S/51",
        # "CNMY18/CS30S/94",
        # "CNMY18/DGJ/07",
        # "CNMY18/DGJ/27",
        # "CNMY18/DGJ/30",
        # "CNMY18/DGJ/32",
        # "CNMY18/DGJ/33",
        # "CNMY18/DGJ/34",
        # "CNMY18/DGJ/36",
        # "CNMY18/DGJ/45",
        # "CNMY18/DGJ/46",
        # "CNMY18/DGJ/47",
        # "CNMY18/IN10S/105",
        # "CNMY18/IN10S/109",
        # "CNMY18/IN10S/22",
        # "CNMY18/IN10S/46",
        # "CNMY18/IN10S/47",
        # "CNMY18/IN10S/71",
        # "CNMY18/IN10S/84",
        # "CNMY18/IN10S/89",
        # "CNMY18/SS00Z/79",
        # "CNMY18/TE00D/20",
        # "CNMY18/TE40S/102",
        # "CNMY18/TE40S/50",
        # "CNMY18/TE40S/52",
        # "CNMY18/TE40S/55",
        # "CNMY18/TE40S/59",
        # "CNMY18/TE40S/61",
        # "CNMY18/TE40S/62",
        # "CNMY18/TE40S/64",
        # "CNMY18/TE40S/65",
        # "CNMY18/TE40S/75",
        # "CNMY18/TE40S/77",
        # "CNMY18/TE40S/90",
        # "CNMY19/03-3/4",
        # "CNMY19/04-4/5",
        # "CNMY19/06-6/53",
        # "CNMY19/18-18/14",
        # "CNMY19/18-18/25",
        # "CNMY19/18-18/61",
        # "CNMY19/AT00A/17",
        # "CNMY19/AT00A/21",
        # "CNMY19/AT00A/27",
        # "CNMY19/AT00A/28",
        # "CNMY19/CS00A/15",
        # "CNMY19/CS30S/11",
        # "CNMY19/CS30S/49",
        # "CNMY19/DGJ/04",
        # "CNMY19/DGJ/08",
        # "CNMY19/DGJ/15",
        # "CNMY19/DGJ/21",
        # "CNMY19/DGJ/22",
        # "CNMY19/DGJ/30",
        # "CNMY19/DGJ/32",
        # "CNMY19/DGJ/34",
        # "CNMY19/DGJ/35",
        # "CNMY19/DGJ/44",
        # "CNMY19/DGPAT/08",
        # "CNMY19/DGPAT/38",
        # "CNMY19/DGPAT/56",
        # "CNMY19/DTVAL/13",
        # "CNMY19/IN10S/36",
        # "CNMY19/IN10S/41",
        # "CNMY19/IN10S/82",
        # "CNMY19/IN10S/86",
        # "CNMY19/IN10S/90",
        # "CNMY19/SG30S/23",
        # "CNMY19/TE10A/46",
        # "CNMY19/TE40S/24",
        # "CNMY19/TE40S/38",
        # "CNMY19/VT00A/25",
        # "CNMY20/0201/227",
        # "CNMY20/0201/24",
        # "CNMY20/0201/3",
        # "CNMY20/0301/59",
        # "CNMY20/19-19/53",
        # "CNMY20/CT00A/12",
        # "CNMY20/DGJ/01",
        # "CNMY20/DGJ/08",
        # "CNMY20/DGJ/10",
        # "CNMY20/DGJ/11",
        # "CNMY20/DGJ/13",
        # "CNMY20/DGJ/14",
        # "CNMY20/DGJ/20",
        # "CNMY20/DGJ/24",
        # "CNMY20/DGJ/25",
        # "CNMY20/DGJ/26",
        # "CNMY20/DGJ/43",
        # "CNMY20/DGJ/43",
        # "CNMY20/DGJ/46",
        # "CNMY20/DGPAT/38",
        # "CNMY20/DGPAT/55",
        # "CNMY20/IN10S/16",
        # "CNMY20/SDGOC/17",
        # "CNMY20/SUBSE/4",
        # "CNMY21/DGJ/01",
        # "CNMY21/DGJ/05",
        # "CNMY21/DGJ/06",
        # "CNMY21/DGJ/10",
        # "CNMY21/DGJ/10",
        # "CNMY21/DGJ/10",
        # "CNMY21/DGJ/11",
        # "CNMY21/DGJ/11",
        # "CNMY21/DGJ/12",
        # "CNMY21/DGJ/14",
        # "CNMY21/DGJ/18",
        # "CNMY21/DGJ/19",
        # "CNMY21/DGJ/27",
        # "CNMY21/DGJ/34",
        # "CNMY21/DGJ/42",
        # "CNMY21/DGJ/44",
        # "CNMY21/DGJ/46",
        # "CNMY21/DGJ/47",
        # "CNMY21/DGJ/50",
        # "CNMY22/DGJ/02",
        # "CNMY22/DGJ/13",
        # "CNMY22/DGJ/28",
        # "CNMY22/DGJ/32",
        # "P.A. 201/2020",
        # "P.A. 354/2018",
        # "P.A.S. 159/2019",
        # "PA 363/2018",
        # "PA. 90/2019",
        # "PA-OB 32/2021",
        # "PAS 268/2019",
        # "PAS 106/2020",
        # "PAS 109/2020",
        # "PAS 110/2019",
        # "PAS 119/2019",
        # "PAS 157 2022",
        # "PAS 232/2022",
        # "PAS 320 2022",
        # "PAS 321/2021",
        # "PAS 393/2022",
        # "PAS 428/2018/TU",
        # "PAS 453 2022",
        # "PAS 454 2022",
        # "PAS 500/2018",
        # "PAS 502/2019",
        # "PAS 531/2019",
        # "PAS 535/2019",
        # "PAS 548/2019",
        # "PAS 576/2020",
        # "PAS 623/2020",
        # "PAS 632 2022",
        # "PAS 701/20",
        # "PAS 72/2020",
        # "PASA 1011/2022 TU",
        # "PASA 969 2022",
        # "PASS 678/2019",
        # "PASS 364/2018",
        # "PASS 404/2019",
        # "PASS 616/2019",
    ]
    for exp in expedientes:
        print("------------------------------------------------")
        print(exp)
        asyncio.run(main(exp))
    """ directory = "../JSONExpedientes/"
    for filename in os.listdir(directory):
        links["Actas de adjudicación"] = []
        links["Actas de valoración de criterios mediante juicio de valor"] = []
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            print(file_path)
            # Read the JSON file
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Modify the JSON data
            print(type(data))
            modified_data = asyncio.run(missing_data(data))

            # Write the modified data back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    modified_data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )
 """
