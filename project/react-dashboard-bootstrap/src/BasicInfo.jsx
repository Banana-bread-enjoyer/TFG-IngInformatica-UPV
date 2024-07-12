import React from "react";
import { Card, Col, Row, ListGroup } from "react-bootstrap";

const BasicInfo = ({ licitacion }) => {
  return (
    <>
      <Card className="mb-4 mt-3">
        <Card.Header as="h4" className="bg-primary text-white">
          Información Básica
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <ListGroup variant="flush">
                <ListGroup.Item>
                  <strong>Número de licitacion:</strong>{" "}
                  {licitacion.num_expediente}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Tipo de Contrato:</strong>{" "}
                  {licitacion.tipo_contrato
                    ? licitacion.tipo_contrato.nombre_tipo_contrato
                    : "N/A"}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Tramitación:</strong>{" "}
                  {licitacion.tramitacion
                    ? licitacion.tramitacion.nombre_tramitacion
                    : "N/A"}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Procedimiento:</strong>{" "}
                  {licitacion.procedimiento
                    ? licitacion.procedimiento.nombre_procedimiento
                    : "N/A"}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Estado:</strong>{" "}
                  {licitacion.estado ? licitacion.estado.estado : "N/A"}
                </ListGroup.Item>

                <ListGroup.Item>
                  <strong>Códigos CPV: </strong>{" "}
                  <ul style={{ listStyleType: "disc" }}>
                    <li>Grupo: {licitacion.clasificacion_grupo || "N/A"}</li>
                    <li>
                      Subgrupo: {licitacion.clasificacion_subgrupo || "N/A"}
                    </li>
                    <li>Categoría: {licitacion.clasificacion_cat || "N/A"}</li>
                  </ul>
                </ListGroup.Item>
              </ListGroup>
            </Col>
            <Col md={6}>
              <ListGroup variant="flush">
                <ListGroup.Item>
                  <strong>Objeto:</strong> {licitacion.objeto || "N/A"}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Unidad Encargada:</strong>{" "}
                  {licitacion.unidad_encargada || "N/A"}
                </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Clasificación Exigida: </strong>{" "}
                  <ul style={{ listStyleType: "disc" }}>
                    <li>Grupo: {licitacion.clasificacion_grupo || "N/A"}</li>
                    <li>
                      Subgrupo: {licitacion.clasificacion_subgrupo || "N/A"}
                    </li>
                    <li>Categoría: {licitacion.clasificacion_cat || "N/A"}</li>
                  </ul>
                </ListGroup.Item>
              </ListGroup>
            </Col>
          </Row>
        </Card.Body>
      </Card>
      <Card className="mb-4">
        <Card.Header as="h4" className="bg-success text-white">
          Criterios y Condiciones
        </Card.Header>
        <Card.Body>
          <Row>
            <ListGroup variant="flush">
              <ListGroup.Item>
                <strong>Mejoras como Criterio de Adjudicación:</strong>{" "}
                {licitacion.mejora_criterio || "N/A"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>Condiciones Especiales:</strong>{" "}
                {licitacion.condiciones_especiales || "N/A"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>
                  {" "}
                  Consideración como Infracción Grave del Incumplimiento de las
                  Condiciones:
                </strong>{" "}
                {licitacion.infraccion_grave || "N/A"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>
                  Contratación del Control de Calidad de la obra mediante un
                  Contrato Independiente:
                </strong>{" "}
                {licitacion.contratacion_control ? "Sí" : "No"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>
                  Inclusión del Control de Calidad en la propia Obra:
                </strong>{" "}
                {licitacion.inclusion_control_calidad ? "Sí" : "No"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>
                  Obligación de indicar en la Oferta si va a haber
                  Subcontratación:
                </strong>{" "}
                {licitacion.obligacion_subcontratacion ? "Sí" : "No"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>
                  Se exige el porcentaje de Subcontratación como Criterio de
                  Adjudicación:
                </strong>{" "}
                {licitacion.subcontratacion_criterio ? "Sí" : "No"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>Porcentaje Máximo de Subcontratación:</strong>{" "}
                {licitacion.porcentaje_max_subcontratacion
                  ? `${licitacion.porcentaje_max_subcontratacion}%`
                  : "N/A"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>
                  Imposición de Penalidades en caso de Incumplimiento de las
                  Condiciones de la Oferta:
                </strong>{" "}
                {licitacion.penalidades_incumplimiento || "N/A"}
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>Acreditar la Solvencia Económica y Financiera</strong>{" "}
                <Row>
                  <Col>
                    <b>Criterios: </b>
                    {licitacion.criterios_economica || "N/A"}
                  </Col>
                  <Col>
                    <b>Medios: </b>
                    {licitacion.medios_economica || "N/A"}
                  </Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <strong>Acreditar la Solvencia Técnica o Profesional</strong>{" "}
                <Row>
                  <Col>
                    <b>Criterios: </b>
                    {licitacion.criterios_tecnica || "N/A"}
                  </Col>
                  <Col>
                    <b>Medios: </b>
                    {licitacion.medios_tecnica || "N/A"}
                  </Col>
                </Row>
              </ListGroup.Item>
            </ListGroup>
          </Row>

          <Card className="mt-3 ps-3 pt-3 pb-3 pe-3">
            <Card.Title>
              Régimen de Penalidades en la Ejecución del Contrato
            </Card.Title>

            <Card.Text>{licitacion.regimen_penalidades || "N/A"}</Card.Text>
          </Card>
          <Card className="mt-3 ps-3 pt-3 pb-3 pe-3">
            <Card.Title>
              Parámetros objetivo para identificar una oferta como anormal
            </Card.Title>

            <Card.Text>
              {licitacion.criterios_valores_anormales || "N/A"}
            </Card.Text>
          </Card>
        </Card.Body>
      </Card>
    </>
  );
};

export default BasicInfo;
