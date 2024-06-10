import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
from io import BytesIO
import fitz
from procesarTextoPDF import separar_por_secciones
from extraerSeccionesLLM import info_sections


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


def contains_text(tag):
    return tag and dato in tag.get_text()


def extraer_info_pliego(data):
    datos = [
        "EXPEDIENTE",
        "OBJETO",
        "LUGAR DE EJECUCIÓN",
        "TIPO DE CONTRATO",
        # "Nº DE LOTES",
        "TRAMITACIÓN",
        "IMPORTE (SIN IMPUESTOS)",
        "IMPORTE",
        "VALOR ESTIMADO DEL CONTRATO",
        "PROCEDIMIENTO",
        "PLAZO DE EJECUCIÓN",
        "CONDICIONES ESPECIALES DE EJECUCIÓN",
        "PLAZO DE PRESENTACIÓN",
        "CLASIFICACIÓN CPV",
    ]
    dict_pliego = {key: None for key in datos}
    """ connection = requests.Session()
    response = connection.get(url) """
    soup = BeautifulSoup(data, "html.parser")
    linkAnexo = ""
    # encontrar primer strong que contiene el expediente´
    for link in soup.findAll("a", href=True):
        if (
            "ANEXO" in link.text.upper()
            and (
                "_I" in link.text.upper()
                or " I " in link.text.upper()
                or " I_" in link.text.upper()
                or "_I_" in link.text.upper()
                or " I.PDF" in link.text.upper()
            )
            and not "BIS" in link.text.upper()
        ):
            response = requests.get(link.get("href"))
            html_pdf = response.content
            soup_pdf = BeautifulSoup(html_pdf, "html.parser")
            link = soup_pdf.find("meta")
            linkAnexo = "https://contrataciondelestado.es" + link.get("content").split(
                "url="
            )[1].strip("'")
            data = requests.get(linkAnexo)
            data = data.content
            doc = fitz.open(stream=data, filetype="pdf")
            dict_anexo = separar_por_secciones(doc)
            if dict_anexo == None:
                return None, None
            dict_anexoLLM = info_sections(doc)
            dict_anexo = {**dict_anexo, **dict_anexoLLM}
            break

    strong = soup.find("strong")
    if strong:
        dict_pliego["EXPEDIENTE"] = strong.text.strip()
    # encontrar primer elemento h2 que contiene el objeto del contrato
    first_h2 = soup.find("h2")
    if first_h2:
        objeto = first_h2.find("div")
        if objeto:
            dict_pliego["OBJETO"] = objeto.text.strip()
    spans = soup.find_all("span")
    for dato in list(dict_pliego.keys())[2:]:
        datoEncontrar = dato.replace("(", "[(]").replace(")", "[)]")
        elem = soup.find(text=re.compile(datoEncontrar, re.IGNORECASE))
        elem = elem.find_parent() if elem else elem

        if elem and dato in elem.text.upper() and not dict_pliego[dato]:
            info = elem.find_next_sibling()
            if info:
                if info.name != "div" and dato == "PLAZO DE PRESENTACIÓN":
                    info = info.find("div")
            else:
                info = elem.find_parent().find_next_sibling()
                if info:
                    info = info.find("div")
                else:
                    info = None
            dict_pliego[dato] = info.text.strip() if info else None
    # SE HA MODIFICADO
    dict_pliego["PLAZO DE PRESENTACIÓN"] = re.sub(
        r".*(\d+\/\d+\/\d+).*", r"\1", dict_pliego["PLAZO DE PRESENTACIÓN"]
    )
    myDict = {**dict_anexo, **dict_pliego}
    # return myDict
    return myDict, linkAnexo
