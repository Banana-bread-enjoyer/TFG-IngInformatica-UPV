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
import FechasyPlazos from "./FechasyPlazos";
import DateRangeIcon from "@mui/icons-material/DateRange";
import InfoIcon from "@mui/icons-material/Info";
import EuroIcon from "@mui/icons-material/Euro";
import AssignmentIcon from "@mui/icons-material/Assignment";
import BasicInfo from "./BasicInfo";
import InsertLinkIcon from "@mui/icons-material/InsertLink";
import CritAdjudicacion from "./CritAdjudicacion";
import LinksDocs from "./LinksDocs";
import ImportesyPagos from "./ImportesyPagos";
const ExpedienteDetails = ({
  empresas,
  participaciones,
  valoraciones,
  tableRefs,
}) => {
  const { expedienteId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  const [licitacion, setLicitacion] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/licitaciones`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        const foundLicitacion = data.find(
          (licitacion) => licitacion.id_licitacion == expedienteId
        );
        setLicitacion(foundLicitacion);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [expedienteId]);

  const handleGoBack = () => {
    navigate(-1); // This navigates back to the previous location
  };

  if (!licitacion) {
    return null; // or loading indicator
  }

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
      <Button variant="secondary" className="ms-2" onClick={handleGoBack}>
        <ArrowBackIcon />
      </Button>
      <Nav
        justify
        variant="tabs"
        className="pt-5"
        activeKey={location.pathname}
      >
        <Nav.Item>
          <Nav.Link as={Link} to="main" active={currentPath.endsWith("/main")}>
            <InfoIcon />
            Información
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link
            as={Link}
            to="fechas"
            active={currentPath.endsWith("/fechas")}
          >
            <DateRangeIcon />
            Fechas y Plazos
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link
            as={Link}
            to="importes"
            active={currentPath.endsWith("/importes")}
          >
            <EuroIcon />
            Importes y Pagos
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link
            as={Link}
            to="criterios"
            active={currentPath.endsWith("/criterios")}
          >
            <AssignmentIcon />
            Criterios de Adjudicación
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link
            as={Link}
            to="links"
            active={currentPath.endsWith("/links")}
          >
            <InsertLinkIcon />
            Links a Documentos
          </Nav.Link>
        </Nav.Item>
      </Nav>

      <Routes>
        <Route path="/" element={<Navigate to="main" />} />
        <Route path="main" element={<BasicInfo licitacion={licitacion} />} />
        <Route
          path="fechas"
          element={<FechasyPlazos licitacion={licitacion} />}
        />
        <Route
          path="importes"
          element={
            <ImportesyPagos
              licitacion={licitacion}
              participaciones={participaciones}
            />
          }
        />
        <Route
          path="criterios"
          element={
            <CritAdjudicacion
              licitacion={licitacion}
              participaciones={participaciones}
              empresas={empresas}
              valoraciones={valoraciones}
              tableRefs={tableRefs}
            />
          }
        />
        <Route path="links" element={<LinksDocs licitacion={expedienteId} />} />
      </Routes>
    </div>
  );
};

export default ExpedienteDetails;
