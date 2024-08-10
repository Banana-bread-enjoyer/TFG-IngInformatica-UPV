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
    extraer_ofertas
    # extract_importes,
)
import csv
import os
from AccessPagePlaywright import scrape_expedientes
from introducirDatosBD import insertar_expediente
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
        "DOC ADMINISTRATIVA"
        "ACTA VALORACIÓN"
        "ACTA APERTURA"
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


async def main():
    expedientes= await scrape_expedientes()
    print("--------------------------------------")
    for expediente, html in expedientes:
        print(expediente)
        links["Actas de adjudicación"] = []
        links["Actas de valoración de criterios mediante juicio de valor"] = []
        try:
            links["Licitación"] = get_link_licitacion(html)
            val = docs_valoraciones(html)
            pliego = acceder_seccion(html, "Pliego")
            if not pliego:
                continue
            infoPliego, linkAnexo = extraer_info_pliego(pliego)
            if infoPliego == None:
                continue
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
            totalDocumentos = list(set(val)|set(docsJuicioValor))
            if len(totalDocumentos)>0:
                infoPliego["OFERTA ECONÓMICA"]=extraer_ofertas(totalDocumentos)
            else:
                infoPliego["OFERTA ECONÓMICA"]=None
            if "SUBCRITERIOS" in infoPliego and infoPliego["SUBCRITERIOS"] and len(docsJuicioValor) > 0:
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
        except:
            print("error, continue loop")
            continue
        # print(myDict)
        save_dict_to_json(
            myDict, "../JSONExpedientes/" + expediente.replace("/", "_") + ".json"
        )
        insertar_expediente(myDict)
        
        


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




# Running the async main function
if __name__ == "__main__":

    asyncio.run(main())
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
