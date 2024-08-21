from datetime import datetime
import json
import os
import pandas as pd
import pyodbc
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from unidecode import unidecode

# Define the connection string
connection_string = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=ASUSMARTA\TFG;"
    r"DATABASE=TFG;"
    r"Trusted_Connection=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


# Function to load JSON data
def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None


# Function to check if a classification exists, and insert if it doesn't
def convertNumber(text):
    if text and type(text) == str:
        num = (
            text.replace("€", "").replace(".", "").replace(",", ".").replace("EUR", "")
        )
        try:
            num = float(num)
            return num
        except:
            return text
    return text


def dict_ofertas(ofertas):
    aux = ofertas
    try:
        for data in ofertas:
            if type(ofertas[data]) == dict:
                for entry in ofertas[data]:
                    if (
                        "IMPORTE" in entry.upper() or "PRECIO" in entry.upper()
                    ) and not " CON " in entry.upper():
                        valor = ofertas[data][entry]
                        aux[data] = convertNumber(valor)
            elif type(ofertas[data]) == str:
                aux[data] = convertNumber(ofertas[data])
    except:
        return None
    return aux


def invert_dict(dictValores):
    inverted_dict = {}
    # Loop through the original dictionary to invert it
    for company, subcriteria in dictValores.items():
        if subcriteria:
            for subcriterion, score in subcriteria.items():
                if subcriterion not in inverted_dict:
                    inverted_dict[subcriterion] = {}
                inverted_dict[subcriterion][company] = score

    # Output the inverted dictionary
    return inverted_dict


def levenshtein_distance(str1, str2):
    # Initialize matrix
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Deletion
                    dp[i][j - 1] + 1,  # Insertion
                    dp[i - 1][j - 1] + 1,
                )  # Substitution

    # The result is the value in the bottom-right corner of the matrix
    return dp[m][n]


def dictValoraciones(dictValores, listCriterios, dictOferta):
    aux = dictValores
    if dictValores:
        for dato in dictValores:
            if aux == dictValores:
                if type(dictValores[dato]) == dict:
                    if "PRECIO" in dato.upper():
                        print("invertir", dato)
                        aux = invert_dict(dictValores)
                        break
                    """ else:
                        for criterio in listCriterios:
                            if dato == criterio["Nombre"] or (
                                "Siglas" in criterio
                                and criterio["Siglas"] != None
                                and criterio["Siglas"] in dato
                            ):
                                print("invertir", dato)
                                aux = invert_dict(dictValores)
                                break """
    return aux


def rename_key(dictionary, old_key, new_key):
    if old_key in dictionary:
        dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def to_bit(text):
    if text != None:
        if type(text) == str:
            if "NO" in text.upper():
                return 0
            elif "SI" in text.upper() or "SÍ" in text.upper():
                return 1
        elif type(text) == bool:
            if text:
                return 1
            else:
                return 0


def find_matching_company(name, existing_companies):
    # Find the best match with a minimum score threshold
    nameNormalized = unidecode(name.upper().replace(",", "").replace(".", ""))
    for nombre in existing_companies:
        if len(name) <= len(nombre) and nameNormalized in unidecode(
            nombre.replace(",", "").replace(".", "")
        ):
            return nombre
        elif (
            len(name) > len(nombre)
            and unidecode(nombre.replace(",", "").replace(".", "")) in nameNormalized
        ):
            return nombre
    matches = process.extract(
        name,
        existing_companies,
        scorer=fuzz.token_sort_ratio,
    )
    if matches and matches[0][1] > 80:  # You can adjust the threshold
        return matches[0][0]
    return None


def match_list(name, list_names):
    try:
        matches = process.extract(
            name,
            list_names,
            scorer=fuzz.token_sort_ratio,
        )
        if matches and matches[0][1] > 80:  # You can adjust the threshold
            return matches[0][0]
        return None
    except:
        return None


def unify_names(dictCriterios, dictOferta):
    listNombresCriterios = list(dictCriterios.keys())
    listNombresOferta = list(dictOferta.keys())
    if len(listNombresCriterios) >= len(listNombresOferta):
        for nombre in listNombresOferta:
            print(nombre, find_matching_company(nombre, listNombresCriterios))
    else:
        for nombre in listNombresCriterios:
            print(nombre, find_matching_company(nombre, listNombresOferta))


def find_corresponding_element(tuples_list, target):
    for tup in tuples_list:
        if target in tup:
            # Return the other element in the tuple
            return tup[1] if tup[0] == target else tup[0]
    return None  # Return None if the target is not found


def agrupar_empresas(dictValoraciones, dictValSubcriterios, dictOfertas, dictAnormales):
    dictionaries = [dictValoraciones, dictValSubcriterios, dictOfertas]
    dictionariesWord = [
        (dictValoraciones, "Criterios"),
        (dictValSubcriterios, "Subcriterios"),
        (dictOfertas, "Oferta"),
    ]
    
    filtered_dictionaries = [d for d in dictionaries if d is not None]
    try:
        largest_dict = max(filtered_dictionaries, key=len)
    except:
        largest_dict=None
    if not largest_dict:
        print("no hay empresas")
        return {}
    dictEmpresas = {
        nombre: {
            "Criterios": None,
            "Subcriterios": None,
            "Oferta": None,
            "Expulsada": 0,
            "AnormalidadEcon": 0,
        }
        for nombre in list(largest_dict.keys())
    }
    # print(dictEmpresas)
    for empresa in largest_dict:
        word = find_corresponding_element(dictionariesWord, largest_dict)
        dictEmpresas[empresa][word] = largest_dict[empresa]
        # nombre subcriterios
        if dictAnormales and type(dictAnormales)==dict:
            nombreAnormales = find_matching_company(empresa, list(dictAnormales.keys()))
            if nombreAnormales:
                dictEmpresas[empresa]["Expulsada"] = 1
                if (
                    "SI" in dictAnormales[nombreAnormales].upper()
                    or "SÍ" in dictAnormales[nombreAnormales].upper()
                ):
                    dictEmpresas[empresa]["AnormalidadEcon"] = 1
        for dictF in filtered_dictionaries:
            # print(dictF)
            if dictF != largest_dict:
                nombre = find_matching_company(empresa, list(dictF.keys()))
                if nombre:
                    word = find_corresponding_element(dictionariesWord, dictF)
                    if nombre in dictF:
                        dictEmpresas[empresa][word] = dictF[nombre]
                    else:
                        dictEmpresas[empresa][word] = None
    return dictEmpresas


def insertar_criterios(dictCriterios, dictSubcriterios, data):
    dictConjunto = {}
    sql_criterios = """
    INSERT INTO Criterios (nombre,siglas,valor_max,valor_min,id_padre)
    VALUES (?,?,?,?,?)
    """
    query = "SELECT id_criterio FROM Criterios WHERE nombre = ? AND valor_max=?"
    idJV = None
    if dictCriterios:
        for criterio in dictCriterios:
            nombre = criterio["Nombre"]
            if not ("INICIAL" in nombre.upper() or "TOTAL" in nombre.upper()):
                valorMax = criterio["Puntuación máxima"]
                if valorMax == None:
                    valorMax = 0
                siglas = criterio["Siglas"]
                valorMin = (
                    criterio["Puntuación Mínima"]
                    if "Puntuación Mínima" in criterio
                    else None
                )
                if all(word in nombre.upper() for word in "JUICIO DE VALOR".split(" ")):
                    if valorMin == None:
                        if valorMax == 40:
                            valorMin = 27
                        elif valorMax == 25:
                            valorMin = 15
                if type(valorMax) == str:
                    valorMax = re.findall(r"\d+", valorMax)[0]
                cursor.execute(query, nombre, valorMax)
                idCriterio = cursor.fetchone()
                if not idCriterio:
                    cursor.execute(sql_criterios, nombre, siglas, valorMax, valorMin, None)
                    conn.commit()
                    cursor.execute(query, nombre, valorMax)
                    idCriterio = cursor.fetchone()
                    if all(word in nombre.upper() for word in "JUICIO DE VALOR".split(" ")):
                        idJV = idCriterio[0]
                if siglas:
                    nombreSiglas = nombre + " (" + siglas + ")"
                else:
                    nombreSiglas = nombre
                dictConjunto[nombreSiglas] = idCriterio[0]
    if dictSubcriterios and data["VALORACIONES SUBCRITERIOS"]:
        for subcriterio in dictSubcriterios:
            nombre = subcriterio["Nombre"]
            valorMax = subcriterio["Puntuación máxima"]
            if valorMax:
                siglas = subcriterio["Siglas"] if "Siglas" in subcriterio else None
                cursor.execute(query, nombre, valorMax)
                idCriterio = cursor.fetchone()
                if not idCriterio:
                    cursor.execute(sql_criterios, nombre, siglas, valorMax, valorMin, idJV)
                    conn.commit()
                    cursor.execute(query, nombre, valorMax)
                    idCriterio = cursor.fetchone()
                    if not siglas:
                        nombreSiglas = nombre
                    else:
                        nombreSiglas = nombre + " (" + siglas + ")"
                    dictConjunto[nombreSiglas] = idCriterio[0]
    return dictConjunto


def insertar_empresa(nombre, pyme, nif, adjudicatario):
    if not nombre:
        return None
    sql_empresas = """
    INSERT INTO Empresas (nombre_empresa,nif,pyme)
    VALUES (?,?,?)
    """
    pyme = to_bit(pyme)
    query = "SELECT id_empresa FROM Empresas WHERE nombre_empresa = ?"
    cursor.execute(query, nombre)
    idEmpresa = cursor.fetchone()
    if not idEmpresa:
        querySimilar = "SELECT nombre_empresa FROM Empresas"
        cursor.execute(querySimilar)
        rows = cursor.fetchall()
        nombres_empresas = []
        for row in rows:
            nombres_empresas.append(row.nombre_empresa)
        nombreDB = match_list(nombre, nombres_empresas)
        if not nombreDB:
            cursor.execute(sql_empresas, nombre, nif, pyme)
            conn.commit()
            cursor.execute(query, nombre)
            idEmpresa = cursor.fetchone()[0]
            return idEmpresa
        else:
            cursor.execute(query, nombreDB)
            idEmpresa = cursor.fetchone()
    idEmpresa = idEmpresa[0]
    if adjudicatario:
        update_query = "UPDATE Empresas SET pyme = ?, nif = ? WHERE id_empresa = ?"
        cursor.execute(update_query, pyme, nif, idEmpresa)
        conn.commit()

    return idEmpresa


def insertar_licitacion(data, idAdjudicatario):
    
    table_name = "Licitaciones"
    cursor.execute(
        f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
    )
    columns = [row.COLUMN_NAME for row in cursor.fetchall()]
    columns.pop(0)
    # Construct the SQL INSERT query dynamically
    column_names = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))

    sql_licitaciones = """
    INSERT INTO Licitaciones ({column_names})
    VALUES ({placeholders})
    """.format(
        column_names=column_names, placeholders=placeholders
    )
    num_expediente = data["EXPEDIENTE"]
    clasificacion = data["CLASIFICACIÓN"]
    cursor.execute(
        "SELECT id_licitacion FROM Licitaciones WHERE num_expediente=?", num_expediente
    )
    idLicitacion = cursor.fetchone()
    if not idLicitacion:
        pattern = re.compile(r"Categoría.*?(\d+)")
        match = pattern.search(clasificacion)
        categoria = None
        if match:
            categoria = match.group(1)
        pattern = re.compile(r"Subgrupo.*?(\d+)")
        match = pattern.search(clasificacion)
        subgrupo = None
        if match:
            subgrupo = match.group(1)
        pattern = re.compile(r"Grupo.*?(\s[A-Z])")
        match = pattern.search(clasificacion)
        grupo = None
        if match:
            grupo = match.group(1).strip()
        condiciones_especiales = (
            data["CONDICIONES ESPECIALES DE EJECUCION A CUMPLIR"]
            if data["CONDICIONES ESPECIALES DE EJECUCION A CUMPLIR"]
            else data["CONDICIONES ESPECIALES DE EJECUCIÓN"]
        )
        cursor.execute(
            "SELECT id_procedimiento FROM TipoProcedimiento WHERE nombre_procedimiento=?",
            data["PROCEDIMIENTO"],
        )
        tipo_procedimiento = cursor.fetchone()[0]
        cursor.execute(
            "SELECT id_tipo_contrato FROM TipoContrato WHERE nombre_tipo_contrato=?",
            data["TIPO DE CONTRATO"],
        )
        tipo_contrato = cursor.fetchone()[0]
        cursor.execute(
            "SELECT id_tramitacion FROM TipoTramitacion WHERE nombre_tramitacion=?",
            data["TRAMITACIÓN"],
        )
        criterios_adjudicacion = (
            data["CRITERIOS DE ADJUDICACION"]
            if "CRITERIOS DE ADJUDICACION" in data
            else data["CRITERIOS DE ADJUDICACION DEL PROCEDIMIENTO ABIERTO"]
        )
        tipo_tramitacion = None
        if data["TRAMITACIÓN"]:
            tipo_tramitacion = cursor.fetchone()[0]
        cursor.execute(
            sql_licitaciones,
            num_expediente,
            data["ABONOS A CUENTA"],
            subgrupo,
            grupo,
            categoria,
            convertNumber(data["IMPORTE"]),
            convertNumber(data["IMPORTE (SIN IMPUESTOS)"]),
            data["CRITERIOS PARA ACREDITAR LA SOLVENCIA ECONOMICA"],
            data["CRITERIOS PARA ACREDITAR LA SOLVENCIA TECNICA"],
            data["CRITERIOS PARA IDENTIFICAR OFERTAS CON VALORES ANORMALES"],
            condiciones_especiales,
            data["CONSIDERACION COMO INFRACCION GRAVE"],
            data["CONTRATACION DEL CONTROL"],
            criterios_adjudicacion,
            data["FECHA ADJUDICACIÓN"],
            data["FECHA FORMALIZACIÓN"],
            data["FECHA ANUNCIO PERFIL DE CONTRATANTE"],
            data["FORMA DE PAGO"],
            data["GARANTIA DEFINITIVA"],
            data["GARANTIA PROVISIONAL"],
            data["GASTOS POR DESISTIMIENTO O RENUNCIA"],
            convertNumber(data["IMPORTES PREVISTOS"]["Modificaciones"]),
            convertNumber(data["IMPORTES PREVISTOS"]["Prórrogas"]),
            convertNumber(data["IMPORTES PREVISTOS"]["Revisión de precios"]),
            convertNumber(data["IMPORTES PREVISTOS"]["Otros Conceptos"]),
            data["INCLUSION DEL CONTROL DE CALIDAD"],
            data["LUGAR DE EJECUCIÓN"],
            data["MEDIOS PARA ACREDITAR LA SOLVENCIA ECONOMICA"],
            data["MEDIOS PARA ACREDITAR LA SOLVENCIA TECNICA"],
            data["MEJORAS COMO CRITERIO DE ADJUDICACION"],
            data["OBJETO"],
            data["OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION"],
            data["OTROS COMPONENTES DEL VALOR ESTIMADO DEL CONTRATO"],
            data["PENALIDADES EN CASO DE INCUMPLIMIENTO DE LAS CONDICIONES"],
            data["PLAZO DE EJECUCIÓN"],
            data["PLAZO DE GARANTIA"],
            datetime.strptime(data["PLAZO DE PRESENTACIÓN"], "%d/%m/%Y").date(),
            data["PLAZO DE RECEPCION"],
            data["PLAZO MAXIMO DE LAS PRORROGAS"],
            data["PLAZO PARA LA PRESENTACION"],
            
            data["POSIBILIDAD DE PRORROGAR EL CONTRATO"],
            tipo_procedimiento,
            
            data["REGIMEN DE PENALIDADES"],
            data["REVISION DE PRECIOS"],
            data["SISTEMA DE PRECIOS"],
            data["SUBASTA ELECTRONICA"],
            data["SUBCONTRATACIÓN COMO CRITERIO"],
            data["TAREAS CRITICAS QUE NO PODRAN SER OBJETO DE SUBCONTRATACION"],
            tipo_contrato,
            tipo_tramitacion,
            data["UNIDAD ENCARGADA DEL SEGUIMIENTO Y EJECUCION"],
            data["VALOR ESTIMADO DEL CONTRATO"],
            idAdjudicatario,
            data["NÚMERO DE EMPRESAS INCURSAS EN ANORMALIDAD"],
            data["NÚMERO DE EMPRESAS INVITADAS"],
            data["NÚMERO DE EMPRESAS SELECCIONADAS"],
            data["NÚMERO DE LICITADORES"],
            data["NÚMERO DE EMPRESAS EXCLUIDAS POR ANORMALIDAD"],
            data["PÁGINA DE INFORMACIÓN DE CRITERIOS"],
            data["PORCENTAJE MAXIMO DE SUBCONTRATACION"],
        )
        conn.commit()
        cursor.execute(
            "SELECT id_licitacion FROM Licitaciones WHERE num_expediente=?",
            num_expediente,
        )
        idLicitacion = cursor.fetchone()
    idLicitacion = idLicitacion[0]
    # insertamos los links en su tabla correspondiente
    sql_links = """
    INSERT INTO Links (link, type_link, id_licitacion)
    VALUES (?,?,?)
    """
    for linkType in data["Links"]:
        cursor.execute(
            "SELECT id_tipo_link FROM TipoLink WHERE texto_tipo_link=?", linkType
        )
        idTipoLink = cursor.fetchone()[0]
        linkList = data["Links"][linkType]
        if type(linkList) == list:
            for link in linkList:
                cursor.execute("SELECT id_link FROM Links WHERE link=?", link)
                idLink = cursor.fetchone()
                if not idLink:
                    cursor.execute(sql_links, link, idTipoLink, idLicitacion)
                    conn.commit()
        elif type(linkList) == str:
            cursor.execute("SELECT id_link FROM Links WHERE link=?", linkList)
            idLink = cursor.fetchone()
            if not idLink:
                cursor.execute(sql_links, linkList, idTipoLink, idLicitacion)
                conn.commit()

    # insertamos los codigos cpv en su tabla correspondiente
    cpvs = data["CLASIFICACIÓN CPV"].strip().split(".")
    sql_cpv = """
    INSERT INTO CodigosCPV(num_cpv,descripcion)
    VALUES (?,?)
    """
    query = "SELECT id_cpv FROM CodigosCPV WHERE num_cpv = ?"
    idCPV = []
    for cpv in cpvs:
        if cpv != "":
            cpv = cpv.split("-")
            cursor.execute(query, cpv[0].strip())
            idcpv = cursor.fetchone()
            if idcpv:
                idCPV.append(idcpv[0])
            else:
                cursor.execute(sql_cpv, cpv[0].strip(), cpv[1].strip())
                conn.commit()
                cursor.execute(query, cpv[0].strip())
                idcpv = cursor.fetchone()
                idCPV.append(idcpv[0])

    # insertamos en la tabla los codigos cpv de la licitacion
    sql_cpvlicitacion = """
    INSERT INTO CPVLicitacion(id_licitacion,id_cpv)
    VALUES (?,?)
    """
    for cpv in idCPV:
        try:
            cursor.execute(sql_cpvlicitacion, idLicitacion, cpv)
            conn.commit()
        except:
            print("Ya existe")
    return idLicitacion


def insertar_participacion_adjudicatario(
    data, idAdjudicatario, idLicitacion, dictEmpresas, idCriterios
):
    sql_participacion = """
    INSERT INTO Participaciones(id_licitacion,id_empresa,importe_ofertado_sin_iva,importe_ofertado_con_iva,excluida,anormalidad_economica)
    VALUES (?,?,?,?,?,?)
    """
    nombreAdjudicatario =data["NOMBRE/RAZÓN SOCIAL ADJUDICATARIO"]
    if dictEmpresas:
        nombreAdjudicatario = find_matching_company(
            data["NOMBRE/RAZÓN SOCIAL ADJUDICATARIO"], list(dictEmpresas.keys())
        )
    if not nombreAdjudicatario:
        nombreAdjudicatario =data["NOMBRE/RAZÓN SOCIAL ADJUDICATARIO"]
    select_participacion = "SELECT id_participacion FROM Participaciones WHERE id_licitacion=? AND id_empresa=?"
    cursor.execute(select_participacion, idLicitacion, idAdjudicatario)
    idParticipacion = cursor.fetchone()
    if not idParticipacion:
        cursor.execute(
            sql_participacion,
            idLicitacion,
            idAdjudicatario,
            data["IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)"],
            data["IMPORTE TOTAL OFERTADO (CON IMPUESTOS)"],
            0,
            data["¿ES LA EMPRESA ADJUDICATARIA ANORMAL?"],
        )
        conn.commit()
        cursor.execute(select_participacion, idLicitacion, idAdjudicatario)
        idParticipacion = cursor.fetchone()
    idParticipacion = idParticipacion[0]
    if dictEmpresas and nombreAdjudicatario in dictEmpresas:
        insertar_valoracion(idCriterios, idParticipacion, dictEmpresas[nombreAdjudicatario])
        dictEmpresas.pop(nombreAdjudicatario)
    return dictEmpresas


def insertar_part_empresas(dictEmpresas, idCriterios, idLicitacion, idAdjudicatario):
    sql_participacion = """
    INSERT INTO Participaciones(id_licitacion,id_empresa,importe_ofertado_sin_iva,importe_ofertado_con_iva,excluida,anormalidad_economica)
    VALUES (?,?,?,?,?,?)
    """
    for empresa in dictEmpresas:
        empresaDict = dictEmpresas[empresa]
        if not empresa:
            return
        idEmpresa = insertar_empresa(empresa, None, None, False)
        if not idEmpresa:
            return
        select_participacion = "SELECT id_participacion FROM Participaciones WHERE id_licitacion=? AND id_empresa=?"
        cursor.execute(select_participacion, idLicitacion, idEmpresa)
        idParticipacion = cursor.fetchone()
        if not idParticipacion:
            conIVA = (
                empresaDict["Oferta"] + empresaDict["Oferta"] * 0.21
                if empresaDict["Oferta"] != None
                and type(empresaDict["Oferta"])==int
                else None
            )
            cursor.execute(
                sql_participacion,
                idLicitacion,
                idEmpresa,
                empresaDict["Oferta"],
                conIVA,
                empresaDict["Expulsada"],
                empresaDict["AnormalidadEcon"],
            )
            conn.commit()
            cursor.execute(select_participacion, idLicitacion, idEmpresa)
            idParticipacion = cursor.fetchone()
        idParticipacion = idParticipacion[0]
        
        insertar_valoracion(idCriterios, idParticipacion, empresaDict)
    return


def insertar_valoracion(idCriterios, idParticipacion, dictEmpresa):
    # print(dictEmpresa)
    sql_valoraciones = """
    INSERT INTO Valoraciones(id_participacion,id_criterio,puntuacion)
    VALUES (?,?,?)
    """
    for criterio in idCriterios:
        cursor.execute(
            "SELECT COUNT(*) FROM Valoraciones WHERE id_participacion=? AND id_criterio=?",
            (idParticipacion, idCriterios[criterio])
        ) 
        exists = cursor.fetchone()[0]
        if exists == 0:
            criteriosEmpr = dictEmpresa["Criterios"]
            if type(criteriosEmpr) == dict:
                for crit in criteriosEmpr:
                    if crit.upper() in criterio.upper():
                        inserted=False
                        if "PCF" in crit.upper() or "FORMULAS" in unidecode(crit.upper()):
                            for critPrecio in criteriosEmpr:
                                if "PRECIO" in crit.upper() or "OFERTA" in crit.upper() or "PCP" in crit.upper() or "ECONOMIC" in unidecode(crit.upper()):
                                    if criteriosEmpr[crit]>criteriosEmpr[critPrecio]:
                                        cursor.execute(
                                            sql_valoraciones,
                                            idParticipacion,
                                            idCriterios[criterio],
                                            criteriosEmpr[crit]-criteriosEmpr[critPrecio],
                                        )
                                        conn.commit()
                                        inserted=True
                                        break
                        if not inserted:
                            try:
                                cursor.execute(
                                    sql_valoraciones,
                                    idParticipacion,
                                    idCriterios[criterio],
                                    criteriosEmpr[crit],
                                )
                                conn.commit()
                            except:
                                 print(f"Error al insertar valoración de {criterio}: {criteriosEmpr[crit]}")
            else:
                cursor.execute(
                    sql_valoraciones,
                    idParticipacion,
                    idCriterios[criterio],
                    criteriosEmpr,
                )
                conn.commit()
            subcriteriosEmpr = dictEmpresa["Subcriterios"]
            if type(subcriteriosEmpr) == dict:
                for crit in subcriteriosEmpr:
                    if crit.upper() in criterio.upper():
                        if type(subcriteriosEmpr[crit]) == str:
                            subcriteriosEmpr[crit] = float(
                                subcriteriosEmpr[crit].replace(",", ".")
                            )
                        cursor.execute(
                            sql_valoraciones,
                            idParticipacion,
                            idCriterios[criterio],
                            subcriteriosEmpr[crit],
                        )
                        conn.commit()


def insertar_expediente(data):
    for item in data:
        aux = data[item]
        if type(aux) == str:
            aux = convertNumber(aux)
            if type(aux) == str:
                aux = aux.replace(
                    "\nPARÁMETROS OBJETIVOS PARA IDENTIFICAR UNA OFERTA COMO ANORMAL:",
                    "",
                )
                aux = aux.replace("☒", "x ")
                aux = re.sub(r"(.*)\nAPARTADO", r"\1", aux)
                if "x No" in aux:
                    aux = re.sub(
                        r"Si\s(?!.*\bSi\s\b).*",
                        "",
                        aux,
                        flags=re.IGNORECASE,
                    )
                    aux = re.sub(
                        r"x (No.*)", r"\1", aux, flags=re.IGNORECASE
                    )
                elif "x Si" in aux:
                    aux = re.sub(
                        r".*x (?=Si(?!.*\bx Si\b))",
                        "",
                        aux,
                        flags=re.IGNORECASE,
                    )
                if "Firmat" in aux:
                    aux = re.sub(r"Firmat.*", "", aux, flags=re.IGNORECASE)
        data[item] = aux

    data["OFERTA ECONÓMICA"] = dict_ofertas(data["OFERTA ECONÓMICA"])
    data["VALORACIONES DE EMPRESAS"] = dictValoraciones(
        data["VALORACIONES DE EMPRESAS"],
        data["CRITERIOS DE ADJUDICACIÓN"],
        data["OFERTA ECONÓMICA"],
    )
    data["VALORACIONES SUBCRITERIOS"] = dictValoraciones(
        data["VALORACIONES SUBCRITERIOS"],
        data["SUBCRITERIOS"],
        data["OFERTA ECONÓMICA"],
    )
    dictEmpresas = agrupar_empresas(
        data["VALORACIONES DE EMPRESAS"],
        data["VALORACIONES SUBCRITERIOS"],
        data["OFERTA ECONÓMICA"],
        data["EMPRESAS EXCLUIDAS POR ANORMALIDAD"],
    )
    data["OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION"] = (
        to_bit(
            data[
                "OBLIGACION DE INDICAR EN LA OFERTA SI VA A HABER SUBCONTRATACION"
            ]
        )
    )
    data["INCLUSION DEL CONTROL DE CALIDAD"] = to_bit(
        data["INCLUSION DEL CONTROL DE CALIDAD"]
    )
    data["SUBASTA ELECTRONICA"] = to_bit(data["SUBASTA ELECTRONICA"])
    data["SUBCONTRATACIÓN COMO CRITERIO"] = to_bit(
        data["SUBCONTRATACIÓN COMO CRITERIO"]
    )
    data["CONTRATACION DEL CONTROL"] = to_bit(data["CONTRATACION DEL CONTROL"])
    data["¿ES LA EMPRESA ADJUDICATARIA ANORMAL?"] = to_bit(
        data["¿ES LA EMPRESA ADJUDICATARIA ANORMAL?"]
    )
    idCriterios = insertar_criterios(
        data["CRITERIOS DE ADJUDICACIÓN"], data["SUBCRITERIOS"], data
    )

    idAdjudicatario = insertar_empresa(
        data["NOMBRE/RAZÓN SOCIAL ADJUDICATARIO"],
        data["EL ADJUDICATARIO ES UNA PYME"],
        data["NIF"],
        True,
    )
    idLicitacion = insertar_licitacion(data, idAdjudicatario)
    if idAdjudicatario:
        dictEmpresas = insertar_participacion_adjudicatario(
            data, idAdjudicatario, idLicitacion, dictEmpresas, idCriterios
        )
        insertar_part_empresas(dictEmpresas, idCriterios, idLicitacion, idAdjudicatario)
    conn.close()
