from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os
import getpass

os.environ["OPENAI_API_KEY"] = (
    "sk-proj-XMk8Yri7a0MR8NapmgT3T3BlbkFJ2RfZ1xorAGApdKQJboKt"
)
# Load PDF document
pdf_path = "DOC202405131105123+PCAP_firmado_PAS+6_2020.pdf"
loader = PyMuPDFLoader(pdf_path)
raw_documents = loader.load()

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(raw_documents)
# Initialize embedding model
""" api_key = "sk-proj-XMk8Yri7a0MR8NapmgT3T3BlbkFJ2RfZ1xorAGApdKQJboKt"
embedding_model = OpenAIEmbeddings(api_key=api_key) """

# Initialize vector store
db = Chroma.from_documents(documents, OpenAIEmbeddings())

# Query function
def query_vector_store(query_text, vector_store):
    """ query_vector = embedding_model.embed_query(query_text) """
    results = vector_store.similarity_search(query_text)
    return results

# Example usage
if __name__ == "__main__":
    query_text = "Abonos a cuentas"
    query_results = query_vector_store(query_text, db)

    # Print or use query results
    print(query_results[0].page_content)

