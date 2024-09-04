import unittest
from bs4 import BeautifulSoup
from extraerAdjudicacion import extraer_fecha, extraer_info_adjudicacion

class TestExtraerAdjudicacion(unittest.TestCase):

    def test_extraer_fecha_correcta(self):
        # HTML simulado con la fecha en el formato correcto
        html = """
        <html>
            <h5>Adjudicación: 23-05-2023</h5>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        fecha = extraer_fecha(soup)
        self.assertEqual(fecha, "23-05-2023")  # Verifica que la fecha extraída es la correcta

    def test_extraer_fecha_incorrecta(self):
        # HTML simulado sin una fecha válida
        html = """
        <html>
            <h5>Adjudicación: Fecha no disponible</h5>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        fecha = extraer_fecha(soup)
        self.assertIsNone(fecha)  # Verifica que la función devuelve None cuando no hay una fecha válida

    def test_extraer_info_adjudicacion_completa(self):
        # HTML simulado con toda la información relevante
        html = """
        <html>
            <h5>Adjudicación: 23-05-2023</h5>
            <h4>Empresa XYZ</h4>
            <ul>
                <li><strong>NOMBRE/RAZÓN SOCIAL ADJUDICATARIO</strong></li>
            </ul>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>12 meses</div>
            <span>NIF</span>
            <div>B12345678</div>
            <span>EL ADJUDICATARIO ES UNA PYME</span>
            <div>Sí</div>
            <span>IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)</span>
            <div>100,000 EUR</div>
            <span>IMPORTE TOTAL OFERTADO (CON IMPUESTOS)</span>
            <div>121,000 EUR</div>
        </html>
        """
        expected_result = {
            "FECHA ADJUDICACIÓN": "23-05-2023",
            "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO": "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO",
            "PLAZO DE EJECUCIÓN": "12 meses",
            "NIF": "B12345678",
            "EL ADJUDICATARIO ES UNA PYME": "Sí",
            "IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)": "100,000 EUR",
            "IMPORTE TOTAL OFERTADO (CON IMPUESTOS)": "121,000 EUR",
        }

        result = extraer_info_adjudicacion(html)
        self.assertEqual(result, expected_result)  # Verifica que toda la información es extraída correctamente

    def test_extraer_info_adjudicacion_incompleta(self):
        # HTML simulado con algunos campos faltantes
        html = """
        <html>
            <h5>Adjudicación: 23-05-2023</h5>
            <h4>Empresa XYZ</h4>
            <ul>
                <li><strong>NOMBRE/RAZÓN SOCIAL ADJUDICATARIO</strong></li>
            </ul>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>12 meses</div>
        </html>
        """
        expected_result = {
            "FECHA ADJUDICACIÓN": "23-05-2023",
            "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO": "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO",
            "PLAZO DE EJECUCIÓN": "12 meses",
            "NIF": None,
            "EL ADJUDICATARIO ES UNA PYME": None,
            "IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)": None,
            "IMPORTE TOTAL OFERTADO (CON IMPUESTOS)": None,
        }
        result = extraer_info_adjudicacion(html)
        self.assertEqual(result, expected_result)  # Verifica que los campos faltantes se devuelven como None

    def test_extraer_info_adjudicacion_sin_fecha(self):
        # HTML simulado sin fecha de adjudicación
        html = """
        <html>
            <h4>Empresa XYZ</h4>
            <ul>
                <li><strong>NOMBRE/RAZÓN SOCIAL ADJUDICATARIO</strong></li>
            </ul>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>12 meses</div>
            <span>NIF</span>
            <div>B12345678</div>
            <span>EL ADJUDICATARIO ES UNA PYME</span>
            <div>Sí</div>
            <span>IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)</span>
            <div>100,000 EUR</div>
            <span>IMPORTE TOTAL OFERTADO (CON IMPUESTOS)</span>
            <div>121,000 EUR</div>
        </html>
        """
        expected_result = {
            "FECHA ADJUDICACIÓN": None,
            "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO": "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO",
            "PLAZO DE EJECUCIÓN": "12 meses",
            "NIF": "B12345678",
            "EL ADJUDICATARIO ES UNA PYME": "Sí",
            "IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)": "100,000 EUR",
            "IMPORTE TOTAL OFERTADO (CON IMPUESTOS)": "121,000 EUR",
        }
        result = extraer_info_adjudicacion(html)
        self.assertEqual(result, expected_result)  # Verifica que la fecha falta y otros campos se extraen correctamente

    def test_extraer_fecha_formato_invalido(self):
        # HTML simulado con una fecha en formato inválido
        html = """
        <html>
            <h5>Adjudicación: 2023/05/23</h5>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        fecha = extraer_fecha(soup)
        self.assertIsNone(fecha)  # Verifica que se devuelve None para formatos de fecha inválidos

    def test_extraer_info_adjudicacion_informacion_extra(self):
        # HTML simulado con información extra que no se espera
        html = """
        <html>
            <h5>Adjudicación: 23-05-2023</h5>
            <h4>Empresa XYZ</h4>
            <ul>
                <li><strong>NOMBRE/RAZÓN SOCIAL ADJUDICATARIO</strong></li>
            </ul>
            <span>PLAZO DE EJECUCIÓN</span>
            <div>12 meses</div>
            <span>NIF</span>
            <div>B12345678</div>
            <span>EL ADJUDICATARIO ES UNA PYME</span>
            <div>Sí</div>
            <span>IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)</span>
            <div>100,000 EUR</div>
            <span>IMPORTE TOTAL OFERTADO (CON IMPUESTOS)</span>
            <div>121,000 EUR</div>
            <!-- Información extra no esperada -->
            <span>INFORMACIÓN EXTRA</span>
            <div>Información no relevante</div>
        </html>
        """
        expected_result = {
            "FECHA ADJUDICACIÓN": "23-05-2023",
            "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO": "NOMBRE/RAZÓN SOCIAL ADJUDICATARIO",
            "PLAZO DE EJECUCIÓN": "12 meses",
            "NIF": "B12345678",
            "EL ADJUDICATARIO ES UNA PYME": "Sí",
            "IMPORTE TOTAL OFERTADO (SIN IMPUESTOS)": "100,000 EUR",
            "IMPORTE TOTAL OFERTADO (CON IMPUESTOS)": "121,000 EUR",
        }
        result = extraer_info_adjudicacion(html)
        self.assertEqual(result, expected_result)  # Verifica que la información extra no afecta el resultado esperado

if __name__ == "__main__":
    unittest.main()
