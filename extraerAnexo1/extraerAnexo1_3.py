import re
import fitz
import pandas as pd
import pprint


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


doc = fitz.open("Anexo1Ejemplo.pdf")  # open a document
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
    linea_actual = lines[i + 1]
    match = re.search(pattern, linea_actual)
    if match:
        return match.group(0)
    else:
        linea = lines[i + 2]
        match = re.search(pattern, linea)
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


# Function to extract categories, groups, and subgroups
def extract_info(input_string):
    category_pattern = r"Categoría\:?\s* (\d+)\.?"
    group_pattern = r"Grupo\:?\s* ([A-Z])\.? ([\w\s]+)\."
    subgroup_pattern = r"Subgrupo\:?\s* (\d+)\.? (.+)\."
    # Initialize an empty dictionary to store the results
    result = {}

    # Extract category
    category_match = re.search(category_pattern, input_string, flags=re.IGNORECASE)
    if category_match:
        category_number = category_match.group(1)
        result["Categoría"] = int(category_number)

    # Extract group
    group_match = re.search(group_pattern, input_string, flags=re.IGNORECASE)
    if group_match:
        group_letter = group_match.group(1)
        group_description = group_match.group(2)
        result["Grupo"] = f"{group_letter}, {group_description}"

    # Extract subgroup
    subgroup_match = re.search(subgroup_pattern, input_string, flags=re.IGNORECASE)
    if subgroup_match:
        subgroup_number = subgroup_match.group(1)
        subgroup_description = subgroup_match.group(2)
        result["Subgrupo"] = f"{subgroup_number}, {subgroup_description}"

    return result


df = pd.read_excel(
    "../NOMBRE_DATOS.xlsx", sheet_name="Hoja1"
)  # can also index sheet by name or fetch all sheets
mylist = df["NOMBRE DATOS"].tolist()
mylist = [x.upper().strip() for x in mylist]
myDict = {key: None for key in mylist}

myDict2 = {
    "CLASIFICACIÓN": "Texto",
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
    "UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCIÓN DEL CONTRATO": "UNA",
    "CONSIDERACIÓN COMO INFRACCIÓN GRAVE": "Texto",
    "GASTOS POR DESISTIMIENTO O RENUNCIA": "Texto",
}

for i in range(len(lines)):
    # Check if the block contains the word
    for dato in myDict:
        if dato in lines[i].upper() and not myDict[dato]:
            if dato == "CLASIFICACIÓN":
                clasificacion = ["GRUPO", "SUBGRUPO", "CATEGORÍA"]
                if all(word in lines[i + 1].upper() for word in clasificacion):
                    possible_lines = lines[i + 1]
                elif any("GRUPO" in line.upper() for line in lines[i + 1 : i + 5]):
                    possible_lines = ".".join(lines[i + 1 : i + 5])
                myDict[dato] = extract_info(possible_lines)
                break
            elif myDict2[dato] == "Valor":
                myDict[dato] = extraer_valor_monetario(i)
                break
            else:
                split = lines[i].split(":")
                if len(split) > 1:
                    resp = split[1]
                else:
                    resp = ""
                j = i + 1
                if (
                    ":" not in lines[i]
                    and lines[j] == lines[j].upper()
                    and "NO" not in lines[j].upper()
                ):
                    j = j + 1
                pattern_no = re.compile(r"X.*[NO,SI].*", re.IGNORECASE)
                if re.match(pattern_no, lines[j]):
                    resp = lines[j].replace("X", "").strip()
                elif re.match(pattern_no, lines[j + 1]):
                    resp = lines[j + 1].replace("X", "").strip()
                else:
                    if resp == "" and lines[j] == lines[j].upper():
                        resp = lines[j]
                        myDict[dato] = resp
                        break
                    while lines[j] != lines[j].upper():
                        resp += " " + lines[j]
                        j += 1
                myDict[dato] = resp
            break


pprint.pprint(myDict)
