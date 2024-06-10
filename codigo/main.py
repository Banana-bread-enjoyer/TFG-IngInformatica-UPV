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
    ]
    documentos = []
    table = soup.find(id="viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux")
    spans = table.find_all("span")
    for span in spans:
        for nombre in nombres:
            # SE HA CAMBIADO
            if all(word in span.text.upper() for word in nombre.split()):
                a = span.find_parent().find_next_sibling().find("a")
                data, link = open_link(a)
                links["Actas de adjudicación"].append(link)
                documentos.append(data)
    documentos.reverse()
    return documentos


def docs_juicio_valor(html):
    nombre = "INFORME DE VALORACIÓN DE LOS CRITERIOS DE ADJUDICACIÓN CUANTIFICABLES MEDIANTE JUICIO DE VALOR"

    soup = BeautifulSoup(html, "html.parser")
    documentos = []
    table = soup.find(id="viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux")
    spans = table.find_all("span")
    for span in spans:
        if nombre in span.text.upper():
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
    formalizacion = acceder_seccion(html, "Formalización")
    soupForm = BeautifulSoup(formalizacion, "html.parser")
    dictFechas["FECHA FORMALIZACIÓN"] = extraer_fecha(soupForm)
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
    a_html = pliego.find_parent().find_next_sibling().find("a")
    data, link = open_link(a_html)
    links[sec] = link
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


def save_dict_to_json(data, file_path):
    """
    Saves a dictionary to a JSON file.

    Parameters:
    data (dict): The dictionary to save.
    file_path (str): The path to the file where the JSON will be saved.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4, sort_keys=True)
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


# Running the async main function
if __name__ == "__main__":
    expedientes = [
        # "CMAYOR/2018/01Y30/53",
        # "CMAYOR/2018/30/15",
        # "CMAYOR/2018/30/17",
        # "CMAYOR/2019/01Y28/66",
        # "CMAYOR/2019/01Y28/91",
        # "CMAYOR/2019/01Y28/94",
        # "CMAYOR/2019/01Y30/142",
        # "CMAYOR/2019/01Y30/144",
        # "CMAYOR/2019/01Y30/6",
        # "CMAYOR/2019/01Y32/45",
        # "CMAYOR/2020/03Y05/114",
        # "CMAYOR/2020/03Y05/32",
        # "CMAYOR/2020/04Y01/28",
        # "CMAYOR/2020/04Y05/6",
        # "CMAYOR/2020/06Y03/71",
        # "CMAYOR/2020/06Y07/152",
        # "CMAYOR/2020/06Y07/27",
        # "CMAYOR/2020/06Y07/30",
        # "CMAYOR/2020/06Y07/36",
        # "CMAYOR/2020/06Y07/77",
        # "CMAYOR/2020/06Y15/120 ",
        # "CMAYOR/2020/06Y15/140",
        # "CMAYOR/2020/06Y15/141",
        "CMAYOR/2020/06Y15/153",
        "CMAYOR/2020/06Y15/154",
        "CMAYOR/2020/06Y15/155",
        "CMAYOR/2020/06Y15/156",
        "CMAYOR/2020/06Y15/25",
        "CMAYOR/2020/06Y15/4",
        "CMAYOR/2020/06Y15/50",
        "CMAYOR/2020/06Y16/27",
        "CMAYOR/2021/03Y03/122",
        "CMAYOR/2021/03Y03/14",
        "CMAYOR/2021/03Y05/71",
        "CMAYOR/2021/03Y05/87",
        "CMAYOR/2021/03Y05/89",
        "CMAYOR/2021/03Y05/97",
        "CMAYOR/2021/04Y01/12",
        "CMAYOR/2021/04Y01/27",
        "CMAYOR/2021/06Y01/31",
        "CMAYOR/2021/06Y03/150",
        "CMAYOR/2021/06Y03/228",
        "CMAYOR/2021/06Y03/230",
        "CMAYOR/2021/06Y03/343",
        "CMAYOR/2021/06Y03/99",
        "CMAYOR/2021/06Y04/126",
        "CMAYOR/2021/06Y04/164",
        "CMAYOR/2021/06Y04/308",
        "CMAYOR/2021/06Y04/56",
        "CMAYOR/2021/06Y04/57",
        "CMAYOR/2021/06Y07/348",
        "CMAYOR/2021/06Y07/356",
        "CMAYOR/2021/06Y07/97",
        "CMAYOR/2021/06Y14/320",
        "CMAYOR/2021/06Y14/78",
        "CMAYOR/2021/07Y10/111",
        "CMAYOR/2021/07Y10/113",
        "CMAYOR/2021/07Y10/121",
        "CMAYOR/2021/07Y10/130",
        "CMAYOR/2021/07Y10/134",
        "CMAYOR/2021/07Y10/136",
        "CMAYOR/2021/07Y10/143",
        "CMAYOR/2021/07Y10/72",
        "CMAYOR/2021/08Y09/250",
        "CMAYOR/2021/08Y09/250",
        "CMAYOR/2021/08Y09/41",
        "CMAYOR/2022/03Y03/86",
        "CMAYOR/2022/03Y05/26",
        "CMAYOR/2022/03Y05/93",
        "CMAYOR/2022/06Y04/194",
        "CMAYOR/2022/06Y14/138",
        "CMAYOR/2022/06Y15/9",
        "CMAYOR/2022/08Y09/114",
        "CMAYOR/2022/08Y09/21",
        "CMAYOR/2022/08Y09/34",
        "CMAYOR/2022/08Y09/34",
        "CMAYOR/2022/12Y03/26",
        "CNMY 134/2022",
        "CNMY 174/2020",
        "CNMY 616/2022",
        "CNMY 689/2021",
        "CNMY 813/2022",
        "CNMY16/VT00A/45",
        "CNMY17/0201/52",
        "CNMY17/0201/66",
        "CNMY17/0201/79",
        "CNMY17/0301/20",
        "CNMY17/0302/154",
        "CNMY17/0303/114",
        "CNMY17/0303/144",
        "CNMY17/0303/145",
        "CNMY17/0303/155",
        "CNMY17/0303/158",
        "CNMY17/0303/162",
        "CNMY17/0303/61",
        "CNMY17/0303/94",
        "CNMY17/0304/160",
        "CNMY17/0304/161",
        "CNMY17/0304/167",
        "CNMY17/18-18/57",
        "CNMY17/18-18/77",
        "CNMY17/AT00A/25",
        "CNMY17/AT00A/27",
        "CNMY17/AT00A/82",
        "CNMY17/CT00A/31",
        "CNMY17/DGJ/49",
        "CNMY17/DGPAT/49",
        "CNMY17/IN10S/21",
        "CNMY17/IN10S/23",
        "CNMY17/SG35S/75",
        "CNMY17/TE00D/64",
        "CNMY17/TE00D/98",
        "CNMY17/TE40S/30",
        "CNMY17/TE40S/61",
        "CNMY17/TE40S/69",
        "CNMY17/TE40S/72",
        "CNMY17/TE40S/73",
        "CNMY17/VT00A/57",
        "CNMY17/VT00A/63",
        "CNMY18/0201/149",
        "CNMY18/0201/2",
        "CNMY18/0201/30",
        "CNMY18/0301/135",
        "CNMY18/0301/147",
        "CNMY18/0301/151",
        "CNMY18/0301/32",
        "CNMY18/0303/10",
        "CNMY18/0303/35",
        "CNMY18/0303/7",
        "CNMY18/03-3/24",
        "CNMY18/03-3/46",
        "CNMY18/06-6/43",
        "CNMY18/06-6/51",
        "CNMY18/06-6/9",
        "CNMY18/12180/008",
        "CNMY18/18-18/10",
        "CNMY18/18-18/7",
        "CNMY18/18-18/8",
        "CNMY18/AT00A/006",
        "CNMY18/AT00A/108",
        "CNMY18/AT00A/74",
        "CNMY18/AT00A/80",
        "CNMY18/AT00A/81",
        "CNMY18/AT00A/82",
        "CNMY18/AT00A/95",
        "CNMY18/AT00A/96",
        "CNMY18/CS00D/18",
        "CNMY18/CS30S/51",
        "CNMY18/CS30S/94",
        "CNMY18/DGJ/07",
        "CNMY18/DGJ/27",
        "CNMY18/DGJ/30",
        "CNMY18/DGJ/30",
        "CNMY18/DGJ/32",
        "CNMY18/DGJ/33",
        "CNMY18/DGJ/34",
        "CNMY18/DGJ/36",
        "CNMY18/DGJ/45",
        "CNMY18/DGJ/46",
        "CNMY18/DGJ/47",
        "CNMY18/DGPAT/23",
        "CNMY18/DTCAS/16",
        "CNMY18/IN10S/105",
        "CNMY18/IN10S/109",
        "CNMY18/IN10S/22",
        "CNMY18/IN10S/46",
        "CNMY18/IN10S/47",
        "CNMY18/IN10S/71",
        "CNMY18/IN10S/84",
        "CNMY18/IN10S/89",
        "CNMY18/SS00Z/79",
        "CNMY18/TE00D/20",
        "CNMY18/TE40S/102",
        "CNMY18/TE40S/50",
        "CNMY18/TE40S/52",
        "CNMY18/TE40S/55",
        "CNMY18/TE40S/59",
        "CNMY18/TE40S/61",
        "CNMY18/TE40S/62",
        "CNMY18/TE40S/64",
        "CNMY18/TE40S/65",
        "CNMY18/TE40S/75",
        "CNMY18/TE40S/77",
        "CNMY18/TE40S/90",
        "CNMY19/0201/104",
        "CNMY19/0201/105",
        "CNMY19/0201/110",
        "CNMY19/0201/111",
        "CNMY19/0201/112",
        "CNMY19/0201/113",
        "CNMY19/0201/114",
        "CNMY19/0201/139",
        "CNMY19/0201/140",
        "CNMY19/0201/17",
        "CNMY19/0201/180",
        "CNMY19/0201/182",
        "CNMY19/0201/94",
        "CNMY19/0301/107",
        "CNMY19/0301/23",
        "CNMY19/0301/36",
        "CNMY19/0301/37",
        "CNMY19/0301/38",
        "CNMY19/0301/40",
        "CNMY19/0301/46",
        "CNMY19/0301/67",
        "CNMY19/0302/92",
        "CNMY19/03-3/4",
        "CNMY19/04-4/5",
        "CNMY19/06-6/53",
        "CNMY19/06-6/78",
        "CNMY19/18-18/14",
        "CNMY19/18-18/25",
        "CNMY19/18-18/61",
        "CNMY19/AT00A/17",
        "CNMY19/AT00A/21",
        "CNMY19/AT00A/27",
        "CNMY19/AT00A/28",
        "CNMY19/CS00A/15",
        "CNMY19/CS30S/11",
        "CNMY19/CS30S/49",
        "CNMY19/DGJ/04",
        "CNMY19/DGJ/08",
        "CNMY19/DGJ/15",
        "CNMY19/DGJ/21",
        "CNMY19/DGJ/22",
        "CNMY19/DGJ/30",
        "CNMY19/DGJ/32",
        "CNMY19/DGJ/34",
        "CNMY19/DGJ/35",
        "CNMY19/DGJ/44",
        "CNMY19/DGPAT/08",
        "CNMY19/DGPAT/38",
        "CNMY19/DGPAT/56",
        "CNMY19/DTVAL/13",
        "CNMY19/IN10S/36",
        "CNMY19/IN10S/41",
        "CNMY19/IN10S/82",
        "CNMY19/IN10S/86",
        "CNMY19/IN10S/90",
        "CNMY19/SG30S/23",
        "CNMY19/TE10A/46",
        "CNMY19/TE40S/24",
        "CNMY19/TE40S/38",
        "CNMY19/VT00A/25",
        "CNMY19/VT00A/29",
        "CNMY19/VT00A/32",
        "CNMY19/VT00A/4",
        "CNMY19/VT00A/55",
        "CNMY19/VT00A/62",
        "CNMY20/00-0/92",
        "CNMY20/00-0/93",
        "CNMY20/00-0/94",
        "CNMY20/0101/5",
        "CNMY20/0201/1",
        "CNMY20/0201/133",
        "CNMY20/0201/134",
        "CNMY20/0201/148",
        "CNMY20/0201/149",
        "CNMY20/0201/150",
        "CNMY20/0201/151",
        "CNMY20/0201/16",
        "CNMY20/0201/19",
        "CNMY20/0201/227",
        "CNMY20/0201/24",
        "CNMY20/0201/3",
        "CNMY20/0201/45",
        "CNMY20/0201/70",
        "CNMY20/0301/109",
        "CNMY20/0301/109",
        "CNMY20/0301/109",
        "CNMY20/0301/109",
        "CNMY20/0301/21",
        "CNMY20/0301/226",
        "CNMY20/0301/226",
        "CNMY20/0301/233",
        "CNMY20/0301/59",
        "CNMY20/0301/59",
        "CNMY20/0301/59",
        "CNMY20/0301/59",
        "CNMY20/0301/59",
        "CNMY20/0301/61",
        "CNMY20/0301/61",
        "CNMY20/0301/61",
        "CNMY20/0301/61",
        "CNMY20/0301/61",
        "CNMY20/0301/9",
        "CNMY20/0304/73",
        "CNMY20/0304/73",
        "CNMY20/19-19/53",
        "CNMY20/CT00A/12",
        "CNMY20/DGJ/01",
        "CNMY20/DGJ/08",
        "CNMY20/DGJ/10",
        "CNMY20/DGJ/11",
        "CNMY20/DGJ/13",
        "CNMY20/DGJ/14",
        "CNMY20/DGJ/20",
        "CNMY20/DGJ/24",
        "CNMY20/DGJ/25",
        "CNMY20/DGJ/26",
        "CNMY20/DGJ/43",
        "CNMY20/DGJ/43",
        "CNMY20/DGJ/46",
        "CNMY20/DGPAT/38",
        "CNMY20/DGPAT/55",
        "CNMY20/IN10S/16",
        "CNMY20/SDGOC/17",
        "CNMY20/SUBSE/4",
        "CNMY21/00-0/1",
        "CNMY21/DGJ/01",
        "CNMY21/DGJ/05",
        "CNMY21/DGJ/06",
        "CNMY21/DGJ/10",
        "CNMY21/DGJ/10",
        "CNMY21/DGJ/10",
        "CNMY21/DGJ/11",
        "CNMY21/DGJ/11",
        "CNMY21/DGJ/12",
        "CNMY21/DGJ/14",
        "CNMY21/DGJ/18",
        "CNMY21/DGJ/19",
        "CNMY21/DGJ/27",
        "CNMY21/DGJ/34",
        "CNMY21/DGJ/42",
        "CNMY21/DGJ/44",
        "CNMY21/DGJ/46",
        "CNMY21/DGJ/47",
        "CNMY21/DGJ/50",
        "CNMY21/DGTIC/56 AM 20/34",
        "CNMY21/DTALI/02",
        "CNMY21/SDGOC/13",
        "CNMY21/SUBSE/12",
        "CNMY21DGJ/53",
        "CNMY22/DGJ/02",
        "CNMY22/DGJ/13",
        "CNMY22/DGJ/15",
        "CNMY22/DGJ/16",
        "CNMY22/DGJ/19",
        "CNMY22/DGJ/20",
        "CNMY22/DGJ/21",
        "CNMY22/DGJ/23",
        "CNMY22/DGJ/27",
        "CNMY22/DGJ/28",
        "CNMY22/DGJ/30",
        "CNMY22/DGJ/31",
        "CNMY22/DGJ/32",
        "CNMY22/DGJ/35",
        "CNMY22/DGJ/35",
        "CNMY22/DGJ/37",
        "CNMY22/DGJ/53",
        "CNMY22/DGJ/54",
        "CNMY22/DGJ/54",
        "CNMY22/DGJ/56",
        "CNMY22/DGJ/60",
        "CNMY22/DGTIC/09 AM 20/34",
        "CNMY22/DGTIC/10 AM20/34",
        "CNMY22/DGTIC/30",
        "NSP 178/2018",
        "NSP 179/2018",
        "P.A. 113/2018",
        "P.A. 145/2018",
        "P.A. 160/2019",
        "P.A. 201/2020",
        "P.A. 264/2022 Lote 1",
        "P.a. 264/2022_Lote 2",
        "P.A. 354/2018",
        "P.A. 451/2018",
        "P.A.S. 159/2019",
        "P.A.S. 585/2022",
        "P.A.S.S. 636/2022",
        "P.N. 151/2018",
        "P.N. 69/2018",
        "PA 363/2018",
        "pa 473/2018",
        "PA 85/2019",
        "PA. 287/2022 TU",
        "PA. 320/2019",
        "PA. 341/2020 TU",
        "PA. 475/2022 TU",
        "PA. 57/2021 TA.TU.",
        "PA. 62/2020 TATU",
        "PA. 7/2018 TA.",
        "PA. 90/2019",
        "PA.409/2019",
        "PA-OB 32/2021",
        "PAS 268/2019",
        "PAS 106/2020",
        "PAS 109/2020",
        "PAS 110/2019",
        "PAS 119/2019",
        "PAS 127/2020",
        "PAS 157 2022",
        "pas 158/2020",
        "PAS 232/2022",
        "PAS 234/2022",
        "PAS 257/2022",
        "PAS 278/2022",
        "PAS 292/2019",
        "PAS 320 2022",
        "PAS 321/2021",
        "PAS 337/2022",
        "PAS 388/2021",
        "PAS 389/2022",
        "PAS 393/2022",
        "PAS 393/2022",
        "PAS 393/2022",
        "PAS 393/2022",
        "PAS 393/2022",
        "PAS 393/2022",
        "PAS 397/2022",
        "PAS 42/2020/TA",
        "PAS 428/2018/TU",
        "PAS 429/2019",
        "PAS 431/2019",
        "PAS 44/2019",
        "PAS 453 2022",
        "PAS 454 2022",
        "PAS 457/2022",
        "PAS 474/2018 TU",
        "PAS 495/2019",
        "PAS 500/2018",
        "PAS 502/2019",
        "PAS 531/2019",
        "PAS 535/2019",
        "PAS 54/2022",
        "PAS 541/2019",
        "PAS 548/2019",
        "PAS 556/2021",
        "PAS 576/2020",
        "PAS 599/2021",
        "PAS 606/2019",
        "PAS 623/2020",
        "PAS 624/2019",
        "PAS 632 2022",
        "PAS 648/2022",
        "PAS 654/2022",
        "PAS 68/2022",
        "PAS 69/2022",
        "PAS 693/2019",
        "PAS 701/20",
        "PAS 72/2020",
        "PAS 767/2021",
        "PAS 776/2021",
        "PAS 777/2021",
        "PAS 782/2021",
        "PAS 788/2021",
        "PAS 800/2021",
        "PAS 808/2022",
        "PAS 815/2021",
        "PAS 877/2022",
        "PAS 88/2021",
        "PAS 897/2022 TU",
        "PAS 906/2022",
        "PAS 918/2022",
        "PAS. 544/2020 TU",
        "PAS. 682/2019",
        "PASA 131 2022",
        "PASA 1011/2022 TU",
        "PASA 969 2022",
        "PASS 678/2019",
        "PASS 135/2022",
        "PASS 233/2022",
        "PASS 364/2018",
        "PASS 404/2019",
        "PASS 616/2019",
        "PASS 876/2022",
        "PASS 94/2022 TA",
        "PN 155/2018",
        "PN 230/2018",
    ]
    for exp in expedientes:
        print("------------------------------------------------")
        print(exp)
        asyncio.run(main(exp))

    # Nombre del archivo CSV
    csv_file = "output_CMAYOR201801Y3063.csv"
    # csv_out = export_dict_to_csv(ejemplo_info, csv_file)
