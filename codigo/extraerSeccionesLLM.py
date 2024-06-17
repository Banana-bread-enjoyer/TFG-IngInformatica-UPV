import fitz  # PyMuPDF
import re
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
import json
from langchain_text_splitters import RecursiveJsonSplitter
from langchain.chains.question_answering import load_qa_chain
import os
from langchain_openai import OpenAI, ChatOpenAI
import tabula
from tabulate import tabulate
import camelot
import ctypes
from ctypes.util import find_library
import pdfplumber
import ast

os.environ["OPENAI_API_KEY"] = (
    "sk-proj-XMk8Yri7a0MR8NapmgT3T3BlbkFJ2RfZ1xorAGApdKQJboKt"
)
llm = ChatOpenAI()
# llm = Ollama(model="llama2:13b")
chat_model = ChatOllama()

prompt = PromptTemplate.from_template(
    """ Answer the question based on the context below.
    Context: {section} 
    Question: {query}
    Answer: """
)


def read_pdf(doc):
    texto_completo = ""
    countPage = 1
    pageLL = None
    for page in doc:
        texto_pagina = page.get_text()
        if not pageLL and "APARTADO LL" in texto_pagina:
            pageLL = countPage
        countPage += 1
        texto_completo += " \n " + texto_pagina
    return texto_completo, pageLL


def extract_sections(text):
    patternApartado = re.compile(r"APARTADO[\s\n]+([A-Z]+)")
    toSplit = re.sub(patternApartado, r"-SPLIT-APARTADO \1", text)
    splited = toSplit.split("-SPLIT-")
    sections = {}
    for section in splited[1:]:
        apartado = re.match(patternApartado, section).group(0)
        contenido = re.sub(patternApartado, "", section)
        sections[apartado] = contenido
    return sections


def info_sections(data):
    dictInfo = {}
    text, page = read_pdf(data)
    sections = extract_sections(text)
    # print(sections)
    promptCriterios = prompt.format(
        section=sections["APARTADO LL"],
        query="Imprime una lista Python en formato [{'Nombre': None, 'Siglas': None, 'Puntuación máxima': None, 'Porcentaje': None}] con todos los criterios principales que se mencionan separados por comas.",
    )
    promptSubcriterios = prompt.format(
        section=sections["APARTADO LL"],
        query="Imprime una lista Python en formato [{'Nombre': None, 'Puntuación máxima': None, 'Porcentaje': None}] con todos los criterios dentro de 'Criterios relacionados con la calidad cuya cuantificación depende de un juicio de valor (PCJ)'.",
    )
    promptSubcontratacion = prompt.format(
        section=sections["APARTADO LL"],
        query="Indica si se exige indicar las empresas que se subontratan (Sí o No)",
    )
    promptClasificacion = prompt.format(
        section=sections["APARTADO L"],
        query="Indica la clasificación. La clasificación consta de Categoría, grupo y subgrupo.",
    )
    promptDetPrecio = prompt.format(
        section=sections["APARTADO E"],
        query="Indica únicamente el tipo de determinación del precio (a tanto alzado, precio unitario u otro, indicar cual). Si hay varios, incluirlos. La X significa que esa es la opción seleccionada",
    )

    subcriterios = llm.invoke(promptSubcriterios).content
    # print(criterios.content)
    if (
        "único criterio" in sections["APARTADO LL"].lower()
        or "único criterio" in sections["APARTADO LL"].lower()
    ):
        dictInfo["CRITERIOS DE ADJUDICACIÓN"] = [
            {"Nombre": "Criterio Precio", "Siglas": "PCP", "Puntuación máxima": 100}
        ]
    else:
        criterios = llm.invoke(promptCriterios)
        criteriosDict = re.sub(r".*(\[.*\]).*", r"\1", criterios.content)
        criteriosDict = criteriosDict.replace("%", "").strip()
        criteriosDict = ast.literal_eval(criteriosDict)
        for criterio in criteriosDict:
            if (
                "precio" in criterio["Nombre"].lower()
                or "econ" in criterio["Nombre"].lower()
            ):
                criterio["Siglas"] = "PCP"
                criterio["Nombre"] = "Puntuación " + criterio["Nombre"]
                break
        dictInfo["CRITERIOS DE ADJUDICACIÓN"] = criteriosDict
    try:
        subcriterios = ast.literal_eval(subcriterios)
        dictInfo["SUBCRITERIOS"] = subcriterios
    except:
        dictInfo["SUBCRITERIOS"] = None

    clasificacion = llm.invoke(promptClasificacion).content
    # criteriosAnorm = llm.invoke(promptAnormales).content
    dictInfo["CRITERIOS PARA IDENTIFICAR OFERTAS CON VALORES ANORMALES"] = sections[
        "APARTADO M"
    ]
    determinacionPrecio = llm.invoke(promptDetPrecio).content
    dictInfo["SISTEMA DE PRECIOS"] = determinacionPrecio

    dictInfo["CLASIFICACIÓN"] = clasificacion
    subcontratacion = llm.invoke(promptSubcontratacion).content
    dictInfo["SUBCONTRATACIÓN COMO CRITERIO"] = subcontratacion
    dictInfo["PÁGINA DE INFORMACIÓN DE CRITERIOS"] = page
    return dictInfo
