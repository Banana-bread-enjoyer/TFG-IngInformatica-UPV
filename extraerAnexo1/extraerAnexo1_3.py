import re
import fitz
import pandas as pd
import pprint


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


doc = fitz.open("Anexo1Ejemplo_2.pdf")  # open a document
lines = []
for page in doc:
    lines.extend(page.get_text().split("\n"))
lines = [line.strip() for line in lines if line.strip() and len(line.strip()) > 1]


def extraer_texto_sección(i, dato):
    block_actual = lines[i]
    block_actual = block_actual.split(dato)
    if len(block_actual) > 1:
        block_actual = block_actual[1]
    else:
        block_actual = block_actual[0]
    resp = ""
    after = block_actual.split(":")
    if len(after) > 1:
        after = block_actual.split(":")[1].replace("\n", " ").strip()
        if after != "":
            resp = after
    j = i + 1
    aux = blocks[j][4].split("(")[0].replace("□", "").strip()
    while aux != aux.upper() or aux == "NO" or aux == "SI":
        resp += " " + blocks[j][4].replace("□", "").strip()
        j += 1
        aux = blocks[j][4].replace("□", "").strip()
    return resp.strip()


def extraer_valor_monetario(i):
    pattern = re.compile(r"\d{1,3}(.\d{3})*,\d+")
    block = lines[i]
    match = re.search(pattern, block)
    if match:
        return match.group(0)
    else:
        block = blocks[i + 1][4]
        match = re.search(pattern, block)
        if match:
            return match.group(0)
    return None


def remove_stopwords(text):
    with open("spanish.txt", "r") as file:
        words_to_remove = {word.strip().upper() for word in file}

    # Split the text into individual words
    words = text.split()

    # Filter out words that are not in the set of words to remove
    filtered_words = [word for word in words if word not in words_to_remove]

    # Join the filtered words back into a string
    new_text = " ".join(filtered_words)
    if "ORDEN" in new_text:
        print(new_text)
    return new_text


df = pd.read_excel(
    "../NOMBRE_DATOS.xlsx", sheet_name="Hoja1"
)  # can also index sheet by name or fetch all sheets
mylist = df["NOMBRE DATOS"].tolist()
mylist = [x.upper().strip() for x in mylist]
myDict = {key: None for key in mylist}

myDict2 = {
    "¿SE HA EXIGIDO ALGUNA CLASIFICACIÓN?": "Texto",
    "MODIFICACIONES PREVISTAS": "Valor",
    "PRÓRROGAS": "Valor",
    "REVISIÓN DE PRECIOS": "Valor",
    "OTROS CONCEPTOS": "Valor",
    "SISTEMA DE PRECIOS": "Texto",
    "SISTEMA DE PRECIOS 2": "Texto",
    "FORMA DE PAGO": "Texto",
    "ABONOS A CUENTA": "SN",
    "¿REVISIÓN DE PRECIOS?": "SN",
    "POSIBILIDAD DE PRORROGAR EL CONTRATO": "SN",
    "PLAZO MÁXIMO DE LAS PRÓRROGAS": "Texto",
    "UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCIÓN DEL CONTRATO": "Texto",
    "CONSIDERACIÓN COMO INFRACCIÓN GRAVE DEL INCUMPLIMIENTO DE LAS CONDICIONES ESPECIALES DE EJECUCIÓN ESTABLECIDAS": "Texto",
    "GASTOS POR DESISTIMIENTO O RENUNCIA": "Texto",
}
print(lines[40])

for i in range(len(lines)):
    # Check if the block contains the word
    for dato in myDict:
        if dato in lines[i].upper() and not myDict[dato]:
            if myDict2[dato] == "Valor":
                resp = None
            else:
                print(dato)
                split = lines[i].split(":")
                if len(split) > 1:
                    resp = split[1]
                else:
                    resp = split[0]
                j = i + 1
                pattern_no = re.compile(r"X\s*[NO,SI].*", re.IGNORECASE)
                if re.match(pattern_no, lines[j]):
                    resp = lines[j].replace("X", "").strip()
                elif re.match(pattern_no, lines[j + 1]):
                    resp = lines[j + 1].replace("X", "").strip()
                else:
                    while lines[j] != lines[j].upper():
                        print(lines[j + 2])
                        resp += " " + lines[j]
                        j += 1
            myDict[dato] = resp


pprint.pprint(myDict)
