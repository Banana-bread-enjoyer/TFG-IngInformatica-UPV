import PyPDF2
import re


def leer_pdf_y_separar_por_secciones(archivo_pdf):
    # Crear un objeto PDFFileReader para leer el PDF
    with open(archivo_pdf, "rb") as archivo:
        lector_pdf = PyPDF2.PdfReader(archivo)
        num_paginas = len(lector_pdf.pages)
        # Inicializar variables para almacenar el texto y las secciones
        texto_completo = ""
        # Leer cada página del PDF
        for pagina_num in range(num_paginas):
            pagina = lector_pdf.pages[pagina_num]
            texto_pagina = (
                pagina.extract_text()
                .replace(":", "\n")
                .replace(" NO ", " No ")
                .replace(" SI ", " Si ")
                .strip()
            )
            texto_completo += (
                texto_pagina  # Agregar el texto de la página al texto completo
            )

        secciones = []
        seccion_actual = ""
        inicio_seccion = False
        for linea in texto_completo.split("\n"):
            if (
                linea.strip().isupper() and not seccion_actual.isupper()
            ):  # Si la línea está en mayúsculas

                if (
                    inicio_seccion
                ):  # Si se ha encontrado el inicio de una nueva sección, agregar la sección anterior a la lista
                    secciones.append(seccion_actual.strip())
                    seccion_actual = ""  # Reiniciar la sección actual
                inicio_seccion = True  # Marcar el inicio de una nueva sección
            seccion_actual += (
                linea + "\n"
            )  # Agregar la línea actual a la sección actual
        # Agregar la última sección a la lista de secciones
        if seccion_actual:
            secciones.append(seccion_actual.strip())

        # Retornar las secciones procesadas
        return secciones


# Ruta al archivo PDF
archivo_pdf = "Anexo1Ejemplo.pdf"

# Leer el PDF y separar por secciones
secciones_pdf = leer_pdf_y_separar_por_secciones(archivo_pdf)
# print(secciones_pdf)
# Imprimir las secciones
for idx, seccion in enumerate(secciones_pdf, start=1):
    print(f"Sección {idx}:")
    print(seccion)
