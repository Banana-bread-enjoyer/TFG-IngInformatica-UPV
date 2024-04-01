import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


def guardar_html_en_archivo(html, nombre_archivo="respuesta.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)


def make_cookies(cookie_dict: dict) -> str:
    return "; ".join(f"{k}={v}" for k, v in cookie_dict.items())


def descargar_pdfs_desde_html(url, expediente):
    connection = requests.Session()
    search_info = {
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1": "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:text71ExpMAQ": expediente,
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menu1MAQ1": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:combo1MAQ": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textLugarEjecucion": "",
        "CpvorigenmultiplecpvMultiple": "FormularioBusqueda",
        "cpvViewmultiplecpvMultiple": "#{beanCpvPpt.cpv}",
        "cpvPrincipalmultiplecpvMultiple": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:cpvMultiple:codigoCpv": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:texOrgContMAQ": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMinFecLimite": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMaxFecLimite": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:texoorganoMAQ": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menuFormaPresentacionMAQ1_SistPresent": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:tipoSistemaContratacion": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menu111MAQ": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:menuTipoTramitacionMAQ": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMinFecAnuncioMAQ2": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMaxFecAnuncioMAQ": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:estadoLici": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:Financiacion": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:texAdjudicatarioMAQ": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:Fuente": "00",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textEstimadoDesde18MAQ": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textEstimado19MAQ": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1": "Buscar",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:idBreadCrumbSeleccionado": "",
        "viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:idControlPulsadoMultiple": "false",
        "javax.faces.ViewState": "j_id99:j_id100",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
        "Referer": "https://contrataciondelestado.es/wps/portal/!ut/p/b1/jZBLr4IwEIV_kZnpUApdllfB-EAqKN3csLi54cbHxvj7LYbEldWzm-T7MicHLPQLJiWXXERxCEewl-E-_g238XoZTtNtxQ_Pt2lalISxCTKkVda2onSnnoTeAWGQ8m7Z1cJUGrEqi2zVshA1ie98fBOFTz8xcawSplCbNUMl8kCEhEwbmn0PMPmqy3eqkgGiTBOkRvFGt0Qoo9l_W5C-6-958ME_gPUjNAO-iZ-AZ8NNeT3_Qu-w6FV1mzTu0bJe72tNDJHDHvoazvZUuMjqnw8PkUsiMA!!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPFormularioBusqueda.jsp/573223473020/-/",
        "Cookie": "JSESSIONID=0000dgKuVkHq8k3D_ogmIY6V4__:prodnod5",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Origin": "https://contrataciondelestado.es",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,es-ES;q=0.9,es;q=0.8",
    }
    response = connection.post(url, data=search_info, headers=headers)
    print(response.status_code)
    guardar_html_en_archivo(response.text)
    soup = BeautifulSoup(response.content, "html.parser")
    linkExpediente = soup.find(
        "a",
        href=lambda href: href
        and href.startswith("https://contrataciondelestado.es/wps/"),
    ).get("href")
    response = requests.get(linkExpediente)
    print(linkExpediente)


url_pagina = "https://contrataciondelestado.es/wps/portal/!ut/p/b1/jZDLboMwEEW_qJrxYAxempchgobiQIs3EYsoSpTHJsr31yCkruLm7kY6R3N1wcL4waTkkosoDuEH7G16no7T43S_TZf5tmLP822aFiVhbIIMqc76XpTu1LMwOiAMUj5shlaYSiNWZZHVPQtRk3jPxxdRuPiJiWOVMIXaNAyVyAMREjJtaPU9wOyrIf9SlQwQZZogdYp3uidCGa3-y4L0Xn_Pg3_8b7B-hFbAN_ECeDb8LO_XA4wOi_6qbpPOPdq0za7VxBA57GBs4GovhYusznz6BaYHauE!/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPFormularioBusqueda.jsp/573220659739/-/"
# Directorio donde se guardarán los PDFs descargados
directorio_destino = "pdfs_descargados"
expediente = "CNMY18/SCAGE/12"
# Crear el directorio de destino si no existe
if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

descargar_pdfs_desde_html(
    "https://contrataciondelestado.es/wps/portal/!ut/p/b1/jZDLboMwEEW_qJrxYAxe2jwMUdIQHEjwpmJRVVR5bKJ8f02ElFXc3N1I52iuLjgYPpiUXHKRpDEcwV3G-_Qz3qbrZTzNtxNfvNhmWVkRpjbKkdZ514nKn2YWBg_EUcb7Vd8IWxvEuirzdcdiNCTe8_FFFD58bdNUaabQ2A1DJYpIxITMWFr8ADD7qi92qpYRosw0Uqt4azoilMnivyxI7_UPPPjHP4ALI7QAoYkfQGDDz-p6_obBY8mz6la3_tGq2ewbQwyRwx4GpeHsTqWPrH_5-AeCmD6c/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPFormularioBusqueda.jsp/573224697512/-/",
    expediente,
)
