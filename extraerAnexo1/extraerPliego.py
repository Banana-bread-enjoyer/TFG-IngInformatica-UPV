import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


def contains_text(tag):
    return tag and dato in tag.get_text()


def extraer_info_pliego(url):
    df = pd.read_excel(
        "../DATOS_PLIEGO.xlsx", sheet_name="Hoja1"
    )  # can also index sheet by name or fetch all sheets
    mylist = df["NOMBRE DATOS"].tolist()
    mylist = [x.upper().strip() for x in mylist]
    myDict = {key: None for key in mylist}
    connection = requests.Session()
    response = connection.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    guardar_html_en_archivo(response.text)
    # encontrar primer strong que contiene el expediente
    strong = soup.find("strong")
    if strong:
        myDict["EXPEDIENTE"] = strong.text.strip()
    # encontrar primer elemento h2 que contiene el objeto del contrato
    first_h2 = soup.find("h2")
    if first_h2:
        objeto = first_h2.find("div")
        if objeto:
            myDict["OBJETO"] = objeto.text.strip()
    spans = soup.find_all("span")
    for dato in list(myDict.keys())[2:]:
        datoEncontrar = dato.replace("(", "[(]").replace(")", "[)]")
        elem = soup.find(text=re.compile(datoEncontrar, re.IGNORECASE))
        elem = elem.find_parent() if elem else elem
        if elem and dato in elem.text.upper() and not myDict[dato]:
            info = elem.find_next_sibling()
            if info:
                if info.name != "div":
                    print("")

            else:
                info = elem.find_parent().find_next_sibling()
                if info:
                    info = info.find("div")
                else:
                    info = None
            myDict[dato] = info.text.strip() if info else None

    print(myDict)


url_pagina = "https://contrataciondelestado.es/wps/wcm/connect/d55c535d-2459-4292-8d61-726f19cecf4c/DOC_CD2021-950337.html?MOD=AJPERES"

extraer_info_pliego(url_pagina)
