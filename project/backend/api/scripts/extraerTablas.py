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
import pandas as pd
import tempfile
import pdfplumber
import ast


os.environ["OPENAI_API_KEY"] = (
    "sk-proj-XMk8Yri7a0MR8NapmgT3T3BlbkFJ2RfZ1xorAGApdKQJboKt"
)
llm = ChatOpenAI(model="gpt-4o-mini")
# model="gpt-4o"
# llm = Ollama(model="llama2:13b")
chat_model = ChatOllama()


def texto_juicio_valor(docs, subcriterios):
    promptValores = PromptTemplate.from_template(
        """ Contesta a la pregunda según el contexto proporcionado.
        Context: {texto} 
        Question: Indica para cada uno de estos criterios la valoración a cada empresa en formato diccionario python: {criterios} 
        Si no aparece algún criterio, poner None

        Answer: """
    )
    dictValoraciones = None
    for doc in docs:
        text, numPages = read_pdf(doc)
        # if all(word in text for word in subcriterios[0].split()):
        # print("ok", numPages)
        if numPages > 3:
            dictValoraciones = extract_table_info(doc, subcriterios)
        else:
            valores = promptValores.format(texto=text, criterios=subcriterios)
            dictValoraciones = llm.invoke(valores)
            dictValoraciones=dictValoraciones.content.replace("`","").replace("python","").split("=")
            if len(dictValoraciones)>1:
                dictValoraciones=dictValoraciones[1]
            else:
                dictValoraciones=dictValoraciones[0]
            dictValoraciones = ast.literal_eval(dictValoraciones.strip())
    # print(dictValoraciones)
    return dictValoraciones


def read_pdf(archivo_pdf):
    doc = fitz.open(stream=archivo_pdf, filetype="pdf")
    texto_completo = ""
    for page in doc:
        texto_pagina = page.get_text()

        texto_completo += " \n " + texto_pagina
    return texto_completo, doc.page_count


def extract_table_info(doc, criterios):
    promptValores = PromptTemplate.from_template(
        """ Contesta a la pregunda según el contexto proporcionado.
        Context: {valoraciones} 
        Question: Indica para cada uno de estos criterios la valoración a cada empresa en formato diccionario python: {criterios} 
        LAS CLAVES DEL DICCIONARIO DEBEN SER LOS NOMBRES DE LAS EMPRESAS
        Si no aparece algún criterio, poner None
        Si aparecen en varias tablas, dar prioridad a las que aparecen antes.

        Answer: """
    )
    if criterios=="IMPORTE OFERTA ECONÓMICA":
        promptValores = PromptTemplate.from_template(
        """ Contesta a la pregunda según el contexto proporcionado.
        Context: {valoraciones} 
        Question: Indica para cada empresa el importe de su oferta económica en euros en formato diccionario Python. La oferta económica es de miles de euros, si no aparece ningún número mayor que 1000, devolver None
        Si no aparece la oferta económica, poner None

        Answer: """
    )

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        temp_pdf.write(doc)
        temp_pdf_path = temp_pdf.name
    pdf_document = fitz.open(temp_pdf_path)
    number_of_pages = pdf_document.page_count
    tablesFile = camelot.read_pdf(
        temp_pdf_path, pages="all", strip_text="\n", flavor="stream"
    )
    tables = ""
    if len(tablesFile) == 0:
        return None
    for table in tablesFile:
        df = table.df
        textTable = table.df.to_string()
        #print(textTable)
        if number_of_pages > 10:
            if (
                (
                    all(
                        word.lower() in textTable.lower()
                        for word in criterios[0].split()
                    )
                    or "puntuación" in textTable.lower()
                )
                and not "BUENO" in textTable
                and df.shape[0] < 40
                and df.shape[1] < 40
            ):
                tables += textTable + "\n------------------------------------------\n"
        elif (
            df.shape[0] >= 2
            and df.shape[1] >= 2
            and df.shape[0] < 50
            and df.shape[1] < 50
        ):
            
            if criterios=="IMPORTE OFERTA ECONÓMICA":
                if "€" in textTable or "IVA" in textTable or re.search(r'\d+\.\d{3}\,\d+', textTable):
                    tables += textTable + "\n------------------------------------------\n"
            else:
                tables += textTable + "\n------------------------------------------\n"
    # print(tables)
    if len(tables) <= 30:
        """ if number_of_pages < 4:
            promptValores = promptValores.format(valoraciones=text, criterios=criterios)
        else: """
        return None
    
    else:
        promptValores = promptValores.format(valoraciones=tables, criterios=criterios)
    respuestaValores = llm.invoke(promptValores)
    valores = respuestaValores.content
    # QUITAR
    if valores.count("None") > len(valores.split("\n"))/3:
        return None
    if (
        not any(
            num in valores for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        )
        or "empresa a" in valores.lower() or "empresa_1" in valores.lower()
    ):
        return None
    # valores = re.sub(r"(IMPORTE[\sA-Za-z\(\)]*\:)\s([\d\.\,]+)\,\n", r"\1 '\2 €'", valores)
    """ valores = re.sub(r"(\d)\.(\d{3})", r"\1\2", valores)
    valores = re.sub(r"(\d)\.(\d{3})\,", r"\1\2.", valores) """
    # valores = re.sub(r"(\d+\.\d+\,\d+)", r"'\1'", valores)
    #valores = re.sub(r"(\d*\.?\d+\.\d+\,\d+)", r"'\1'", valores)
  
    dictValores=valores.replace("`","").replace("python","").replace("\n","").split("=")

    if len(dictValores)>1:
        dictValores=dictValores[1]
    else:
        dictValores=dictValores[0]
    return ast.literal_eval(dictValores.strip())

 
def extract_text(doc):
    dictEmpresas = {
        "NÚMERO DE EMPRESAS INVITADAS": None,
        "NÚMERO DE LICITADORES": None,
        "NÚMERO DE EMPRESAS SELECCIONADAS": None,
        "NÚMERO DE EMPRESAS INCURSAS EN ANORMALIDAD": None,
        "NÚMERO DE EMPRESAS EXCLUIDAS POR ANORMALIDAD": None,
        "¿ES LA EMPRESA ADJUDICATARIA ANORMAL?": None,
        "EMPRESAS EXCLUIDAS POR ANORMALIDAD": None,
    }
    promptInfoEmpresas = PromptTemplate.from_template(
        """ Contesta a la pregunda según el contexto proporcionado.
        Context: {texto} 
        Question: Completa el siguiente diccionario con la información que se pide: {dict}
        Si algún dato no se encuentra dejar None
        El número de empresas invitadas suele ser 0, a no ser que se especifique otra cosa. 
        El número de licitadores son el número de EMPRESAS MENCIONADAS
        El número de empresas incursas en anormalidad es el número de empresas que se han considerado anormales, tanto las que se han aceptado como las que no
        En Empresas excluidas incluir un diccionario con el nombre de la empresa excluida y un string (SI o NO) que indica SI SE HAN EXCLUIDO POR criterio económico
        Answer: """
    )
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
        temp_pdf.write(doc)
        temp_pdf_path = temp_pdf.name
    text = ""
    with pdfplumber.open(temp_pdf_path) as pdf:
        for page in pdf.pages:
            # Extract the entire text
            page_text = page.extract_text()
            text += "\n" + page_text

    promptInfoEmpresas = promptInfoEmpresas.format(texto=text, dict=dictEmpresas)
    respuestaEmpresas = llm.invoke(promptInfoEmpresas)
    respuestaEmpresas=respuestaEmpresas.content
    respuestaEmpresas = (
        respuestaEmpresas.replace(": No,", ': "No",')
        .replace(": Sí", ': "Sí"')
        .replace(": SI", ': "Sí"')
        .replace(": NO", ': "No"')
    )
    respuestaEmpresas=respuestaEmpresas.replace("`","").replace("python","").split("=")
    if len(respuestaEmpresas)>1:
        respuestaEmpresas=respuestaEmpresas[1]
    else:
        respuestaEmpresas=respuestaEmpresas[0]
    print(respuestaEmpresas)
    dictValEmpresas = ast.literal_eval(respuestaEmpresas.strip())
    print(dictValEmpresas)
    countEcon = 0
    empresasExcluidas = dictValEmpresas["EMPRESAS EXCLUIDAS POR ANORMALIDAD"]
    print(empresasExcluidas)
    return dictValEmpresas

def extraer_ofertas(docs):
    dictImporte = None
    for doc in docs:
        if dictImporte == None:
            dictImporte = extract_table_info(doc, "IMPORTE OFERTA ECONÓMICA")
    return dictImporte

def extraer_info_acta(docs, nombres):
    dictInfoEmpresas = None
    dictValoraciones = None
    
    # print(docs)
    for doc in docs:
        if dictValoraciones == None:
            dictValoraciones = extract_table_info(doc, nombres)
        if dictInfoEmpresas == None:
            dictInfoEmpresas = extract_text(doc)
    if dictInfoEmpresas == None:
        dictInfoEmpresas = {
            "NÚMERO DE EMPRESAS INVITADAS": None,
            "NÚMERO DE LICITADORES": None,
            "NÚMERO DE EMPRESAS SELECCIONADAS": None,
            "NÚMERO DE EMPRESAS INCURSAS EN ANORMALIDAD": None,
            "NÚMERO DE EMPRESAS EXCLUIDAS POR ANORMALIDAD": None,
            "¿ES LA EMPRESA ADJUDICATARIA ANORMAL?": None,
            "EMPRESAS EXCLUIDAS POR ANORMALIDAD": None,
        }

    return {
        "VALORACIONES DE EMPRESAS": dictValoraciones,
        **dictInfoEmpresas,
    }
