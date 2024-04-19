import fitz
import re
import nltk
from nltk.tokenize import sent_tokenize
import time
import pprint

start = time.time()
datos = [
    "CLASIFICACIÓN",
    "VALOR ESTIMADO DEL CONTRATO",
    "DETERMINACIÓN DEL PRECIO",
    "FORMA DE PAGO",
    "ABONOS A CUENTA",
    "POSIBILIDAD DE PRORROGAR EL CONTRATO",
    "PLAZO MÁXIMO DE LAS PRÓRROGAS",
    "UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCIÓN",
    "CONSIDERACIÓN COMO INFRACCIÓN GRAVE",
    "GASTOS POR DESISTIMIENTO O RENUNCIA",
]
dictDatos = {key: None for key in datos}


def leer_pdf_y_separar_por_secciones(archivo_pdf):
    pattern = re.compile(r"([A-Z]?[a-z]+)\s*\n\s*([A-Z]+)")
    pattern2 = re.compile(r"([A-Z]+)\s*\n\s*([A-Z])([a-z]+)")
    patternApartado = re.compile(r"APARTADO[\s\n]*[A-Z]")
    patternParentesis = re.compile(r"([A-Z]+)\s*\(([a-zA-Z]+.*?)\)")
    # Crear un objeto PDFFileReader para leer el PDF
    with fitz.open(archivo_pdf) as doc:
        # Inicializar variables para almacenar el texto y las secciones
        texto_completo = ""
        # Leer cada página del PDF
        for page in doc:
            texto_pagina = (
                page.get_text()
                .replace(".\n", ". \n")
                .replace(":", ". ")
                .replace("Sí", "Si")
                .replace(" No ", " No ")
                .replace("□", "")
                .strip()
            )
            texto_completo += re.sub(
                patternApartado, "", texto_pagina
            )  # Agregar el texto de la página al texto completo

        modified_text = re.sub(pattern, r"\1. \2", texto_completo)
        # print(modified_text)
        modified_text = re.sub(pattern2, r"\1. \2\3", modified_text)
        modified_text = re.sub(patternParentesis, r"\1. ", modified_text)
        tokens = modified_text.split(". ")
        # print(re.sub(pattern, r"\1. \2", "vilidad\nATRIB"))
        # print(tokens)
        secciones = {}
        current_key = None

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
    print(dictDatos)


# Ruta al archivo PDF
archivo_pdf = "Anexo1Ejemplo.pdf"

# Leer el PDF y separar por secciones
secciones_pdf = leer_pdf_y_separar_por_secciones(archivo_pdf)
guardar_secciones_de_datos(secciones_pdf)
# print(secciones_pdf)
# Imprimir las secciones
end = time.time()
print(end - start)
