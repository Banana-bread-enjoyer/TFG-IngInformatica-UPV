import re
import fitz


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


import pandas as pd

df = pd.read_excel(
    "../NOMBRE_DATOS.xlsx", sheet_name="Hoja1"
)  # can also index sheet by name or fetch all sheets
mylist = df["NOMBRE DATOS"].tolist()
mylist = [x.upper().strip() for x in mylist]
myDict = {key: False for key in mylist}
doc = fitz.open("Anexo1Ejemplo.pdf")  # open a document
blocks = []
for page in doc:
    blocks = blocks + page.get_text("blocks")
pattern_objetoContrato = re.compile(r"OBJETO DEL CONTRATO.*?\n(.*?)\n\n")
for i in range(len(blocks)):
    # Check if the block contains the word
    for dato in mylist:
        if dato in blocks[i][4].upper() and not myDict[dato]:
            if (
                dato == "VALOR ESTIMADO DEL CONTRATO"
                or dato == "MODIFICACIONES PREVISTAS"
            ):
                pattern = re.compile(r"\d{1,3}(.\d{3})*(,\d+)?")
                block = blocks[i][4]
                match = re.search(pattern, block)
                if match:
                    print(dato, ": ", match.group(0))
                else:
                    block = blocks[i + 1][4]
                    match = re.search(pattern, block)
                    if match:
                        print(dato, ": ", match.group(0))
            else:
                pattern_linea = re.compile(r"[a-zA-z]")
                if ": No" in blocks[i][4]:
                    resp = "No"
                # Extract text from the block after the block containing the word
                else:
                    resp = blocks[i + 1][4]
                    resp = re.sub("□", "", resp).strip()
                    if resp == "No" or resp == "No procede":
                        resp = "No"
                    else:
                        j = i + 2
                        while blocks[j][4] != blocks[j][4].upper():
                            resp += blocks[j][4]
                            j += 1
                print(dato, ": ", resp)
            myDict[dato] = True
