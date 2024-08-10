import fitz
import re
import nltk
from nltk.tokenize import sent_tokenize
import time
import pprint
from unidecode import unidecode
from PIL import Image
import pytesseract
import io
from extraerSeccionesLLM import info_sections

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def is_scanned_page(page):
    """Determine if a PDF page is scanned by checking if text extraction yields minimal or no text."""
    text = page.get_text()

    # Threshold for considering a page as scanned
    if len(text.strip()) < 20:
        return True
    return False


def extract_text_from_scanned_page(page):
    """Extract text from a scanned PDF page using OCR."""
    pix = page.get_pixmap()  # Render page to an image
    image = Image.open(io.BytesIO(pix.tobytes()))  # Convert to PIL Image
    return pytesseract.image_to_string(image)


def separar_por_secciones(doc):
    datos = [
        "VALOR ESTIMADO DEL CONTRATO",
        "FORMA DE PAGO",
        "POSIBILIDAD DE PRORROGAR EL CONTRATO",
        "PLAZO MAXIMO DE LAS PRORROGAS",
        #"UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCION",
        #"CONSIDERACION COMO INFRACCION GRAVE",
        #"GASTOS POR DESISTIMIENTO O RENUNCIA",
        #"CONTRATACION DEL CONTROL",
        #"INCLUSION DEL CONTROL DE CALIDAD",
        "PLAZO DE GARANTIA",
        "GARANTIA PROVISIONAL",
        "GARANTIA DEFINITIVA",
        "REGIMEN DE PENALIDADES",
        #"SUBASTA ELECTRONICA",
        "PLAZO PARA LA PRESENTACION",
        #"PLAZO DE RECEPCION",
        #"OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION",
        #"PENALIDADES EN CASO DE INCUMPLIMIENTO DE LAS CONDICIONES",
        #"TAREAS CRITICAS QUE NO PODRAN SER OBJETO DE SUBCONTRATACION",
        "CONDICIONES ESPECIALES DE EJECUCION A CUMPLIR",
        #"REVISION DE PRECIOS",
        "IMPORTE",
        #"CRITERIOS DE ADJUDICACION DEL PROCEDIMIENTO ABIERTO",
        "PORCENTAJE MAXIMO DE SUBCONTRATACION",
        #"MEJORAS COMO CRITERIO DE ADJUDICACION",
        "CRITERIOS PARA ACREDITAR LA SOLVENCIA ECONOMICA",
        "MEDIOS PARA ACREDITAR LA SOLVENCIA ECONOMICA",
        "CRITERIOS PARA ACREDITAR LA SOLVENCIA TECNICA",
        "MEDIOS PARA ACREDITAR LA SOLVENCIA TECNICA",
        "OTROS COMPONENTES DEL VALOR ESTIMADO DEL CONTRATO",
    ]

    pattern = re.compile(
        r"([A-ZÁÉÍÓÚ]?[a-záéíóú]+).?[\s\n]*\n[\s\n]*([A-ZÁÉÍÓÚ]{2,20}\s)"
    )
    pattern2 = re.compile(
        r"([A-ZÁÉÍÓÚ]+)[\s\n]*\n[\s\n]*([^A-Za-z]*\s*[A-ZÁÉÍÓÚ])([a-záéíóú]+)"
    )
    patternApartado = re.compile(r"APARTADO[\s\n]*[A-Z]")
    patternParentesis = re.compile(r"([A-ZÁÉÍÓÚ]+)\s*\((.+\n.+)\)")
    patternSeleccion = re.compile(r"([A-ZÁÉÍÓÚ]+)[\s\n]*\n[\s\n]*([Xx]\s*)")
    patternFooter1 = re.compile(r"CSV\:.*")
    patternFooter2 = re.compile(r"URL de validaci.*\:.*")
    patternHeader1 = re.compile(
        r"Direcció General d’Obres Públiques, Transports\ni Mobilitat Sostenible"
    )
    patternHeader2 = re.compile(r"CIUTAT ADMINISTRATIVA.*\n.*Tel.*\d*")
    patternPage = re.compile(r"\b\d+\b(?![\s\S]*[\d\w]+)")
    patternPage2 = re.compile(r"\b\d+\b\s*\n\s*")
    patternSi = re.compile(r"([^\n\s\w\d])\s*SI")
    patternNo = re.compile(r"([Xx□])\s*NO")
    patternPuntos = re.compile(r"([A-Z]+)\:(.*)")
    patternNumPrimero = re.compile(r"([A-Z]+)\n+([^a-zA-Z]+\s*[a-z\s]+)")
    # Crear un objeto PDFFileReader para leer el PDF
    # Inicializar variables para almacenar el texto y las secciones
    texto_completo = ""
    # Leer cada página del PDF
    pageLL = None
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Check if the page is scanned
        if is_scanned_page(page):
            texto_pagina = extract_text_from_scanned_page(page)
            return None
        else:
            texto_pagina = page.get_text()
        if "APARTADO LL" in texto_pagina:
            pageLL = page_num

        texto_pagina = re.sub(patternFooter1, "", texto_pagina)
        texto_pagina = re.sub(patternFooter2, "", texto_pagina)
        texto_pagina = re.sub(patternHeader1, "", texto_pagina)
        texto_pagina = re.sub(patternHeader2, "", texto_pagina)
        texto_pagina = re.sub(patternPage, "", texto_pagina)
        texto_pagina = re.sub(patternSi, r"\1 Si", texto_pagina)
        texto_pagina = re.sub(patternNo, r"\1 No", texto_pagina)
        texto_pagina = re.sub(r"(DETERMINACIÓN DEL PRECIO)\n", r"\1: ", texto_pagina)
        texto_pagina = re.sub(patternPuntos, r"\1. \2", texto_pagina)
        texto_pagina = re.sub(patternNumPrimero, r"\1. \2", texto_pagina)
        # texto_pagina = re.sub(patternSpaces, r"\1 \2", texto_pagina)

        # print(texto_pagina)
        texto_pagina = (
            texto_pagina.replace(".\n", ". \n")
            # .replace(":", ". ")
            .replace("NO PROCEDE", "No procede")
            .replace(" SI.", " Si ")
            .replace("[X]", "x ")
            .replace("[x]", "x ")
            .replace("X ", "x ")
            .replace("X  ", "x ")
            .replace("☑", "x")
            .replace("\nX", "\nx")
            .replace("□", "")
            .replace("ART.", "ART")
            .replace("TANTO ALZADO", "tanto alzado")
            .replace("PRECIOS UNITARIOS", "precios unitarios")
            .replace("GRUPO", "Grupo")
            .replace("SUBGRUPO", "Subgrupo")
            .replace("CATEGORIA", "Categoria")
            .replace("\n NO", "\n no")
            .replace("\n SÍ", "\n si")
            .replace("\n SI", "\n si")
            .replace("1.", "a 1.")
            .strip()
        )
        texto_completo += " \n " + re.sub(
            patternApartado, ". ", texto_pagina
        )  # Agregar el texto de la página al texto completo
    modified_text = re.sub(pattern, r"\1. \2", texto_completo)
    modified_text = re.sub(r"OBSERVACIONES", ". ", modified_text)
    # print(modified_text)
    modified_text = re.sub(pattern2, r"\1. \2\3", modified_text)
    modified_text = re.sub(patternParentesis, r"\1. ", modified_text)
    modified_text = re.sub(patternSeleccion, r"\1. \2", modified_text)

    # modified_text = re.sub(pattern3, r"\1. \2", modified_text)
    tokens = modified_text.split(". ")
    # print(re.sub(pattern, r"\1. \2", "vilidad\nATRIB"))
    # print(tokens)
    secciones = {}
    current_key = None
    # print(tokens[806])
    for sentence in tokens:
        if sentence.isupper():
            current_key = sentence.replace("\n", " ").strip().upper()
            secciones[current_key] = ""
        elif current_key:
            secciones[current_key] += sentence.strip() + ". "

    # Retornar las secciones procesadas
    dict_secciones = guardar_secciones_de_datos(secciones, datos, pageLL)
    dict_secciones["IMPORTES PREVISTOS"] = dict_secciones.pop("IMPORTE")
    dict_secciones.pop("VALOR ESTIMADO DEL CONTRATO")

    return dict_secciones


def guardar_secciones_de_datos(secciones, datos, pageLL):
    dictDatos = {key: None for key in datos}
    for seccion in secciones:
        for dato in datos:
            if not dictDatos[dato] and all(
                word in unidecode(seccion) for word in dato.split()
            ):
                info = secciones[seccion]
                if dato == "IMPORTE":
                    info = sacar_valores_previstos(info)
                dictDatos[dato] = info
    dictDatos["PÁGINA DE INFORMACIÓN DE CRITERIOS"] = pageLL
    # print(secciones)
    return dictDatos


def sacar_valores_previstos(texto):
    patterns = {
        "Modificaciones": r"Modificaciones[^0-9]*\n([\d.,]+)",
        "Prórrogas": r"Prórrogas[^0-9]*\n([\d.,]+)",
        "Revisión de precios": r"Revisión de precios[^0-9]*\n([\d.,]+)",
        "Otros Conceptos": r"Otros Conceptos[^0-9]*\n([\d.,]+)",
    }
    previstos = {}
    for pat in patterns:
        match = re.search(patterns[pat], texto)
        if match:
            # Extract the matched group
            matched_group = match.group(1)
            previstos[pat] = matched_group
        else:
            previstos[pat] = "0,00"
    return previstos
