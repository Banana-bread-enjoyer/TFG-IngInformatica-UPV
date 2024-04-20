import fitz
import re
import nltk
from nltk.tokenize import sent_tokenize
import time
import pprint
import unicodedata

start = time.time()
datos = [
    "CLASIFICACION",
    "VALOR ESTIMADO DEL CONTRATO",
    "DETERMINACION DEL PRECIO",
    "FORMA DE PAGO",
    "ABONOS A CUENTA",
    "POSIBILIDAD DE PRORROGAR EL CONTRATO",
    "PLAZO MAXIMO DE LAS PRORROGAS",
    "UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCION",
    "CONSIDERACION COMO INFRACCION GRAVE",
    "GASTOS POR DESISTIMIENTO O RENUNCIA",
    "CONTRATACION DEL CONTROL",
    "INCLUSION DEL CONTROL DE CALIDAD",
    "PLAZO DE GARANTIA",
    "GARANTIA PROVISIONAL",
    "GARANTIA DEFINITIVA",
    "REGIMEN DE PENALIDADES",
    "SUBASTA ELECTRONICA",
    "PLAZO PARA LA PRESENTACION",
    "PLAZO DE RECEPCION",
    "OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION",
    "PENALIDADES EN CASO DE INCUMPLIMIENTO DE LAS CONDICIONES",
    "TAREAS CRITICAS QUE NO PODRAN SER OBJETO DE SUBCONTRATACION",
]
dictDatos = {key: None for key in datos}


def leer_pdf_y_separar_por_secciones(archivo_pdf):
    pattern = re.compile(r"([A-Z]?[a-z]+).?[\s\n]*\n[\s\n]*([A-ZÁÉÍÓÚ]{2,15}\s)")
    pattern2 = re.compile(r"([A-Z]+)[\s\n]*\n[\s\n]*([^A-Za-z]*\s*[A-Z])([a-z]+)")
    patternApartado = re.compile(r"APARTADO[\s\n]*[A-Z]")
    patternParentesis = re.compile(r"([A-Z]+)\s*\(([a-zA-Z]+.*?)\)")
    patternSeleccion = re.compile(r"([A-Z]+)[\s\n]*\n[\s\n]*([Xx]\s*)")
    patternFooter1 = re.compile(r"CSV\:.*")
    patternFooter2 = re.compile(r"URL de validación\:.*")
    patternPage = re.compile(r"^\s+\d{1,2}\s+")
    patternSi = re.compile(r"([Xx□])\s*SI")
    patternNo = re.compile(r"([Xx□])\s*NO")
    # Crear un objeto PDFFileReader para leer el PDF
    with fitz.open(archivo_pdf) as doc:
        # Inicializar variables para almacenar el texto y las secciones
        texto_completo = ""
        # Leer cada página del PDF
        for page in doc:
            texto_pagina = re.sub(patternPage, "", page.get_text())
            texto_pagina = re.sub(patternFooter1, "", texto_pagina)
            texto_pagina = re.sub(patternFooter2, "", texto_pagina)
            texto_pagina = re.sub(patternSi, r"\1 Si", texto_pagina)
            texto_pagina = re.sub(patternNo, r"\1 No", texto_pagina)
            texto_pagina = (
                texto_pagina.replace(".\n", ". \n")
                .replace(":", ". ")
                .replace("NO PROCEDE", "No procede")
                .replace(" SI.", " Si ")
                .replace("□", "")
                .replace("TANTO ALZADO", "tanto alzado")
                .replace("PRECIOS UNITARIOS", "precios unitarios")
                .strip()
            )
            texto_completo += re.sub(
                patternApartado, ". ", texto_pagina
            )  # Agregar el texto de la página al texto completo
        texto_completo = "".join(
            c
            for c in unicodedata.normalize("NFD", texto_completo)
            if unicodedata.category(c) != "Mn"
        )
        modified_text = re.sub(pattern, r"\1. \2", texto_completo)
        # print(modified_text)
        modified_text = re.sub(pattern2, r"\1. \2\3", modified_text)
        modified_text = re.sub(patternParentesis, r"\1. ", modified_text)
        modified_text = re.sub(patternSeleccion, r"\1. \2", modified_text)
        # modified_text = re.sub(pattern3, r"\1. \2", modified_text)
        tokens = modified_text.split(". ")
        # print(re.sub(pattern, r"\1. \2", "vilidad\nATRIB"))
        print(tokens)
        secciones = {}
        current_key = None
        # print(tokens[806])
        for sentence in tokens:
            if sentence.isupper():
                current_key = sentence.replace("\n", " ").strip().upper()
                secciones[current_key] = ""
            elif current_key:
                secciones[current_key] += sentence.replace("\n", " ").strip() + ". "

        # Retornar las secciones procesadas
        return secciones


def guardar_secciones_de_datos(secciones):
    for seccion in secciones:
        for dato in datos:
            if not dictDatos[dato] and dato in seccion:
                dictDatos[dato] = secciones[seccion]
    pprint.pprint(dictDatos)


# Ruta al archivo PDF
archivo_pdf = "Anexo1Ejemplo_3.pdf"

# Leer el PDF y separar por secciones
secciones_pdf = leer_pdf_y_separar_por_secciones(archivo_pdf)
guardar_secciones_de_datos(secciones_pdf)
# print(secciones_pdf)
# Imprimir las secciones
end = time.time()
print(end - start)
