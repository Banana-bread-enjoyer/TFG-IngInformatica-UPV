import React, { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import Button from "react-bootstrap/Button";
import { useNavigate } from "react-router-dom";
import { Card, Container, Row, Col } from "react-bootstrap";
import { MDBTypography } from "mdb-react-ui-kit";
import { Nav } from "react-bootstrap";
import { Link, Routes, Route, Navigate } from "react-router-dom";
import "./ExpedienteDetails.css";

const FechasyPlazos = ({ licitacion }) => {
  const location = useLocation();
  const formatDate = (dateString) => {
    const options = { day: "2-digit", month: "2-digit", year: "numeric" };
    return new Date(dateString).toLocaleDateString("es-ES", options);
  };
  // Format ampliacion_presentacion
  let ampliacionPresentacion = licitacion.ampliacion_presentacion;
  if (
    ampliacionPresentacion.charAt(ampliacionPresentacion.length - 1) === "."
  ) {
    ampliacionPresentacion = ampliacionPresentacion.slice(0, -1);
  }
  if (
    ampliacionPresentacion.charAt(ampliacionPresentacion.length - 2) === "."
  ) {
    ampliacionPresentacion = ampliacionPresentacion.slice(0, -2);
  }
  let lines = ampliacionPresentacion.split(".");
  if (lines.length === 1) {
    lines = lines[0].split("\n");
  }

  const currentPath = location.pathname;

  return (
    <div className="ms-3 mt-3 me-3">
      <Container fluid className="mt-3 py-5">
        <Row>
          <Col lg="12">
            <div className="horizontal-timeline">
              <MDBTypography listInLine className="items">
                {licitacion.fecha_anuncio && (
                  <li className="items-list">
                    <div className="px-4">
                      <div className="event-date badge bg-info">
                        {formatDate(licitacion.fecha_anuncio)}
                      </div>
                      <h5 className="pt-2">Fecha de Anuncio</h5>
                    </div>
                  </li>
                )}
                {licitacion.plazo_presentacion && (
                  <li className="items-list">
                    <div className="px-4">
                      <div className="event-date badge bg-success">
                        {formatDate(licitacion.plazo_presentacion)}
                      </div>
                      <h5 className="pt-2">Fecha de Presentación</h5>
                    </div>
                  </li>
                )}
                {licitacion.fecha_adjudicacion && (
                  <li className="items-list">
                    <div className="px-4">
                      <div className="event-date badge bg-danger">
                        {formatDate(licitacion.fecha_adjudicacion)}
                      </div>
                      <h5 className="pt-2">Fecha de Adjudicación</h5>
                    </div>
                  </li>
                )}
                {licitacion.fecha_formalizacion && (
                  <li className="items-list">
                    <div className="px-4">
                      <div className="event-date badge bg-warning">
                        {formatDate(licitacion.fecha_formalizacion)}
                      </div>
                      <h5 className="pt-2">Fecha de Formalización</h5>
                    </div>
                  </li>
                )}
              </MDBTypography>
            </div>
          </Col>
        </Row>
      </Container>

      <Container fluid className="py-3">
        <Row>
          {licitacion.plazo_ejecucion && (
            <Col md="4">
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>Plazo de Ejecución</Card.Title>
                  <Card.Text>{licitacion.plazo_ejecucion}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
          )}
          {licitacion.plazo_garantia && (
            <Col md="4">
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>Plazo de Garantía</Card.Title>
                  <Card.Text>{licitacion.plazo_garantia}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
          )}
          {licitacion.plazo_recepcion && (
            <Col md="4">
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>Plazo de Recepción</Card.Title>
                  <Card.Text>{licitacion.plazo_recepcion}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
          )}
          {licitacion.plazo_maximo_prorrogas && (
            <Col md="4">
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>Plazo de Máximo de las Prórrogas</Card.Title>
                  <Card.Text>{licitacion.plazo_maximo_prorrogas}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
          )}
          {licitacion.ampliacion_presentacion && (
            <Col md="4">
              <Card className="mb-3">
                <Card.Body>
                  <Card.Title>
                    Ampliación de la Presentación de Ofertas
                  </Card.Title>
                  <Card.Text>
                    {lines.map((line, index) => (
                      <React.Fragment key={index}>
                        {line}
                        <br />
                      </React.Fragment>
                    ))}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          )}
        </Row>
      </Container>
    </div>
  );
};

export default FechasyPlazos;
