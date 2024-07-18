import React from "react";
import { Card, Col, Row, ListGroup } from "react-bootstrap";

const ImportesyPagos = ({ licitacion, participaciones }) => {
  return (
    <>
      <Card className="mb-4 mt-3">
        <Card.Header as="h4" className="bg-primary text-white"></Card.Header>
        <Card.Body>
          <ListGroup variant="flush">
            <ListGroup.Item>
              <strong>Presupuesto Base de licitacion:</strong>{" "}
              <ul>
                <li>
                  <b>Importe sin IVA: </b>{" "}
                  {parseFloat(licitacion.importe_sin_impuestos).toLocaleString(
                    "es-ES",
                    {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    }
                  )}
                </li>
                <li>
                  <b>Importe con IVA: </b>{" "}
                  {parseFloat(licitacion.importe_con_impuestos).toLocaleString(
                    "es-ES",
                    {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    }
                  )}
                </li>
              </ul>
              <strong>Valor estimado del Contrato:</strong>{" "}
              {parseFloat(licitacion.valor_estimado).toLocaleString("es-ES", {
                style: "currency",
                currency: "EUR",
                minimumFractionDigits: 2,
              })}
              <ul>
                <li>
                  <b>Modificaciones Previstas: </b>{" "}
                  {parseFloat(licitacion.modificaciones_prev).toLocaleString(
                    "es-ES",
                    {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    }
                  )}
                </li>
                <li>
                  <b>Prórrogas Previstas: </b>{" "}
                  {parseFloat(licitacion.prorrogas_prev).toLocaleString(
                    "es-ES",
                    {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    }
                  )}
                </li>
                <li>
                  <b>Revision de Precios Previstas: </b>{" "}
                  {parseFloat(licitacion.revision_precios_prev).toLocaleString(
                    "es-ES",
                    {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    }
                  )}
                </li>
                <li>
                  <b>Otros Conceptos Previstos: </b>{" "}
                  {parseFloat(licitacion.otros_conceptos_prev).toLocaleString(
                    "es-ES",
                    {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    }
                  )}
                </li>
              </ul>
              <strong>
                Otros componentes del valor estimado del Contrato:
              </strong>{" "}
              {licitacion.otros_componentes ? licitacion.otros_componentes : ""}
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Abonos a Cuenta:</strong>{" "}
              {licitacion.abonos_cuenta ? licitacion.abonos_cuenta : ""}
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Garantías:</strong>
              <ul>
                <li>
                  <strong>Garantía Definitiva:</strong>{" "}
                  {licitacion.garantia_def ? licitacion.garantia_def : ""}
                </li>
                <li>
                  <strong>Garantía Provisional:</strong>{" "}
                  {licitacion.garantia_prov ? licitacion.garantia_prov : ""}
                </li>
              </ul>
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>
                Importe de los Gastos por Desistimiento o Renuncia:
              </strong>{" "}
              {licitacion.gastos_desistimiento
                ? licitacion.gastos_desistimiento
                : ""}
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Sistema de Precios:</strong>{" "}
              {licitacion.sistema_precios ? licitacion.sistema_precios : ""}
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Subasta Electrónica:</strong>{" "}
              {licitacion.subasta_electronica ? "Sí" : "No"}
            </ListGroup.Item>
          </ListGroup>
        </Card.Body>
      </Card>
    </>
  );
};

export default ImportesyPagos;
