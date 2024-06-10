import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
from io import BytesIO
import fitz


def extraer_fecha(soup):
    # encontrar primer h5 para fecha de adjudicacion
    h5 = soup.find("h5")
    if h5:
        fecha = re.search(r"\d+\-\d+\-\d+", h5.text.strip())
        if fecha:
            fecha = fecha.group(0)
    return fecha


def extraer_info_adjudicacion(data):
    datos = [
        "FECHA ADJUDICACIÓN",
        "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO",
        "PLAZO DE EJECUCIÓN",
        "NIF",
        "EL ADJUDICATARIO ES UNA PYME",
        "IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)",
        "IMPORTE TOTAL OFERTADO (CON IMPUESTOS)",
    ]
    dict_adjudicacion = {key: None for key in datos}
    soup = BeautifulSoup(data, "html.parser")
    # encontrar primer h5 para fecha de adjudicacion
    fecha = extraer_fecha(soup)
    dict_adjudicacion["FECHA ADJUDICACIÓN"] = fecha
    adjudicatario = soup.find("h4")
    if adjudicatario:
        nombre = adjudicatario.find_next_sibling("ul")
        if nombre:
            nombre = nombre.find("strong")
            if nombre:
                dict_adjudicacion["NOMBRE/RAZÓN SOCIAL ADJUDICATARIO"] = nombre.text
    # encontrar primer elemento h2 que contiene el objeto del contrato
    for span in soup.find_all("span"):
        text = span.text.upper().strip()
        if text in datos:
            info = span.find_next_sibling("div")
            if info:
                info = info.text.strip().strip(":").strip()
            else:
                info = span.find_parent().find_next_sibling().find("div").text.strip()
            dict_adjudicacion[text] = info
    return dict_adjudicacion
