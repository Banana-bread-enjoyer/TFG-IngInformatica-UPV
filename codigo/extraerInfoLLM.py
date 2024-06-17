# Importing required functionalities
import fitz
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from typing_extensions import Concatenate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyMuPDFLoader, PyPDFDirectoryLoader
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import os
from langchain_community.callbacks import get_openai_callback
from langchain_community.document_loaders import TextLoader
import pinecone
from langchain_chroma import Chroma
import re
from langchain_community.llms import Ollama

os.environ["OPENAI_API_KEY"] = (
    "sk-proj-XMk8Yri7a0MR8NapmgT3T3BlbkFJ2RfZ1xorAGApdKQJboKt"
)
llm = Ollama(model="llama2:13b")
llm = OpenAI()
chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125")


def read_pdf(archivo_pdf):
    doc = fitz.open(archivo_pdf)
    texto_completo = ""
    for page in doc:
        texto_pagina = page.get_text()

        texto_completo += " \n " + texto_pagina
    return texto_completo


def split_text(text):
    text_chunker = RecursiveCharacterTextSplitter(
        separators=["\n \n", "\n\n", "\n", ".", ","],
        chunk_size=800,
        chunk_overlap=200,
        length_function=len,
    )
    text_sections = text_chunker.split_text(text)
    return text_sections


def answer_query(query, vector):
    docs = vector.similarity_search(query)
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.invoke({"input_documents": docs, "question": query})
    return response


pdf_text = read_pdf("Anexo1Ejemplo.pdf")
text_sections = split_text(pdf_text)
vector = Chroma.from_texts(text_sections, OpenAIEmbeddings())
query = (
    "Indica los criterios de adjudicación con su desglose y sus máximas puntuaciones"
)
response = answer_query(query, vector)
print(response)
