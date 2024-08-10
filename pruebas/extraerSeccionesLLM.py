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
llm = ChatOpenAI(model="gpt-4o-mini")
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
    if "APARTADO LL" not in sections:
        sections["APARTADO LL"]=sections["APARTADO L"]
    # print(sections)
    promptCriterios = prompt.format(
        section=sections["APARTADO LL"],
        query="Imprime una lista Python en formato [{'Nombre': None, 'Siglas': None, 'Puntuación máxima': None, 'Puntuación mínima': None}] con los criterios principales separados por comas.",
    )
    promptSubcriterios = prompt.format(
        section=sections["APARTADO LL"],
        query="Imprime una lista Python en formato [{'Nombre': None, 'Puntuación máxima': None}] con todos los subcriterios dentro de 'Criterios relacionados con la calidad cuya cuantificación depende de un juicio de valor' o los apartados de la memoria que no sean sub indices como 1.1 ni sub sub indices como 1.1.1 .",
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
    promptAbonoCuentas = prompt.format(
        section=sections["APARTADO W"],
        query="Indica si se exigen abonos a cuenta (Sí o No)",
    )
    promptUnidad = prompt.format(
        section=sections["APARTADO T"],
        query="Indica ÚNICAMENTRE la unidad encargada del seguimiento y ejecución del contrato sin texto adicional",
    )
    dictInfo["UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCION"]=llm.invoke(promptUnidad).content
    promptInfraccionGrave=prompt.format(
        section=sections["APARTADO T"],
        query="Indica la consideración como infracción grave del inclumplimiento de las condiciones especiales de ejecución (Sí o No)",
    )
    dictInfo["CONSIDERACION COMO INFRACCION GRAVE"]=llm.invoke(promptInfraccionGrave).content
    promptContratacionControl=prompt.format(
        section=sections["APARTADO Y"],
        query="Indica si hay CONTRATACIÓN DEL control de calidad de la obra mediante un contrato independiente (Sí o No)",
    )
    dictInfo["CONTRATACION DEL CONTROL"]=llm.invoke(promptContratacionControl).content
    promptGastos=prompt.format(
        section=sections["APARTADO Y"],
        query="Indica el texto del apartado de IMPORTE DE GASTOS POR DESISTIMIENTO O RENUNCIA",
    )
    dictInfo["GASTOS POR DESISTIMIENTO O RENUNCIA"]=llm.invoke(promptGastos).content
    promptInclusionControl=prompt.format(
        section=sections["APARTADO Y"],
        query="Indica si hay INCLUSIÓN DEL CONTROL DE CALIDAD EN LA PROPIA OBRA (Sí o No)",
    )
    dictInfo["INCLUSION DEL CONTROL DE CALIDAD"]=llm.invoke(promptInclusionControl).content
    promptCriteriosNum=prompt.format(
        section=sections["APARTADO D"],
        query="Indica el número de criterios (Varios criterios o único criterio precio) sin texto introductorio",
    )
    dictInfo["CRITERIOS DE ADJUDICACION DEL PROCEDIMIENTO ABIERTO"]=llm.invoke(promptCriteriosNum).content
    promptMejora=prompt.format(
        section=sections["APARTADO LL"],
        query="Indica si hay MEJORAS COMO CRITERIO DE ADJUDICACIÓN (Sí o No)",
    )
    dictInfo["MEJORAS COMO CRITERIO DE ADJUDICACION"]=llm.invoke(promptMejora).content
    promptObligacionSubcontrata=prompt.format(
        section=sections["APARTADO Q"],
        query="Indica si hay OBLIGACIÓN DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACIÓN (Sí o No)",
    )
    dictInfo["OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION"]=llm.invoke(promptObligacionSubcontrata).content
    promptPenalidades=prompt.format(
        section=sections["APARTADO T"],
        query="Indica las Penalidades por incumplimiento de las condiciones especiales de ejecución",
    )
    dictInfo["PENALIDADES EN CASO DE INCUMPLIMIENTO DE LAS CONDICIONES"]=llm.invoke(promptPenalidades).content
    promptPlazoRecepcion=prompt.format(
        section=sections["APARTADO U"],
        query="Indica el plazo de recepción",
    )
    dictInfo["PLAZO DE RECEPCION"]=llm.invoke(promptPlazoRecepcion).content
    promptRevision=prompt.format(
        section=sections["APARTADO H"],
        query="Indica si hay revisión de precios y el motivo",
    )
    dictInfo["REVISION DE PRECIOS"]=llm.invoke(promptRevision).content
    promptSubasta=prompt.format(
        section=sections["APARTADO H"],
        query="Indica si hay subasta electrónica (Sí o No)",
    )
    dictInfo["SUBASTA ELECTRONICA"]=llm.invoke(promptSubasta).content
    promptTareasCriticas=prompt.format(
        section=sections["APARTADO Q"],
        query="Indica si hay TAREAS CRITICAS QUE NO PODRÁN SER OBJETO DE SUBCONTRATACIÓN (Sí o No) y si las hay, cuáles",
    )
    dictInfo["TAREAS CRITICAS QUE NO PODRAN SER OBJETO DE SUBCONTRATACION"]=llm.invoke(promptTareasCriticas).content
    subcriteriosLLM = llm.invoke(promptSubcriterios)
    subcriterios = subcriteriosLLM.content.replace("`","").replace("python","").replace("\n","").split("=")

    if len(subcriterios)>1:
        subcriterios=subcriterios[1].strip()
    else:
        subcriterios=subcriterios[0].strip()
    # print(criterios.content)
    
    criteriosLLM = llm.invoke(promptCriterios)
    criteriosDict=criteriosLLM.content.replace("`","").replace("python","").replace("\n","").split("=")

    if len(criteriosDict)>1:
        criteriosDict=criteriosDict[1].strip()
    else:
        criteriosDict=criteriosDict[0].strip()
    criteriosDict = ast.literal_eval(criteriosDict)
    dictInfo["CRITERIOS DE ADJUDICACIÓN"] = criteriosDict
    
    subcriterios = ast.literal_eval(subcriterios)
    dictInfo["SUBCRITERIOS"] = subcriterios
    

    clasificacion = llm.invoke(promptClasificacion).content
    # criteriosAnorm = llm.invoke(promptAnormales).content
    dictInfo["CRITERIOS PARA IDENTIFICAR OFERTAS CON VALORES ANORMALES"] = sections[
        "APARTADO M"
    ]
    dictInfo["ABONOS A CUENTA"]=llm.invoke(promptAbonoCuentas).content
    determinacionPrecio = llm.invoke(promptDetPrecio).content
    dictInfo["SISTEMA DE PRECIOS"] = determinacionPrecio

    dictInfo["CLASIFICACIÓN"] = clasificacion
    subcontratacion = llm.invoke(promptSubcontratacion).content
    dictInfo["SUBCONTRATACIÓN COMO CRITERIO"] = subcontratacion
    dictInfo["PÁGINA DE INFORMACIÓN DE CRITERIOS"] = page
    match = re.search(r'RÉGIMEN DE PENALIDADES.*?\n(.*?)CONSIDERACIÓN COMO INFRACCIÓN GRAVE', sections["APARTADO T"], re.DOTALL | re.IGNORECASE)
    if match:
        dictInfo["REGIMEN DE PENALIDADES"]=match.group(1).strip()
    return dictInfo
