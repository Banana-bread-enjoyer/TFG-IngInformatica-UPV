import React, { useEffect, useState } from "react";
import { Link, Routes, Route, useLocation, Navigate } from "react-router-dom";
import { Nav } from "react-bootstrap";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import EqualizerIcon from "@mui/icons-material/Equalizer";
import TableComponent from "./TableComponent.jsx";
import SearchBar from "./SearchBar.jsx";
import { parse, compareAsc } from "date-fns";
import { es } from "date-fns/locale";
import StatsLicitaciones from "./StatsLicitaciones.jsx";
const TabLicitaciones = ({ valoraciones, participaciones, empresas }) => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState(null);
  const [licitaciones, setLicitaciones] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/licitaciones/")
      .then((response) => response.json())
      .then((data) => {
        setLicitaciones(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const applyFilters = (newFilters) => {
    setFilters(newFilters);
  };

  const checkFiltros = (licitacion) => {
    if (filters) {
      if (
        filters.lugarEjecucion &&
        !licitacion.lugar_ejecucion
          .toLowerCase()
          .includes(filters.lugarEjecucion.toLowerCase())
      ) {
        return false;
      }

      if (
        filters.importeMax &&
        parseFloat(licitacion.importe_sin_impuestos) >
          parseFloat(filters.importeMax)
      ) {
        return false;
      }
      if (
        filters.importeMin &&
        parseFloat(licitacion.importe_sin_impuestos) <
          parseFloat(filters.importeMin)
      ) {
        return false;
      }
      if (
        filters.unidadEncargada &&
        !licitacion.unidad_encargada
          .toLowerCase()
          .includes(filters.unidadEncargada.toLowerCase())
      ) {
        return false;
      }
      if (filters.plazoPresentacionDesde) {
        const dateLicitacion = parse(
          licitacion.plazo_presentacion,
          "dd/MM/yyyy",
          new Date()
        );
        const dateFiltro = parse(
          filters.plazoPresentacionDesde,
          "yyyy-MM-dd",
          new Date()
        );
        if (dateLicitacion < dateFiltro) {
          return false;
        }
      }
      if (filters.plazoPresentacionHasta) {
        const dateLicitacion = parse(
          licitacion.plazo_presentacion,
          "dd/MM/yyyy",
          new Date()
        );
        const dateFiltro = parse(
          filters.plazoPresentacionHasta,
          "yyyy-MM-dd",
          new Date()
        );
        if (dateLicitacion > dateFiltro) {
          return false;
        }
      }
      if (filters.estado && filters.estado != licitacion.estado.id_estado) {
        return false;
      }
      if (
        filters.tipoContrato &&
        filters.tipoContrato != licitacion.tipo_contrato.id_tipo_contrato
      ) {
        return false;
      }
      if (
        filters.tipoProcedimiento &&
        filters.tipoProcedimiento != licitacion.procedimiento.id_procedimiento
      ) {
        return false;
      }
      if (
        filters.tipoTramitacion &&
        filters.tipoTramitacion != licitacion.tramitacion.id_tramitacion
      ) {
        return false;
      }
    }

    return true;
  };

  const filteredLicitaciones = licitaciones.filter(
    (licitacion) =>
      Object.values(licitacion).some(
        (value) =>
          typeof value === "string" &&
          value.toLowerCase().includes(searchQuery.toLowerCase())
      ) && checkFiltros(licitacion)
  );

  return (
    <>
      <div className="mb-3">
        <SearchBar
          className="pt-5"
          setSearchQuery={setSearchQuery}
          applyFilters={applyFilters}
        />
        <Nav
          justify
          variant="tabs"
          className="pt-5"
          activeKey={location.pathname}
        >
          <Nav.Item>
            <Nav.Link
              as={Link}
              to="list"
              active={location.pathname === "/licitaciones/list"}
            >
              <FormatListBulletedIcon /> Lista
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              as={Link}
              to="stats"
              active={location.pathname === "/licitaciones/stats"}
            >
              <EqualizerIcon /> Estadísticas
            </Nav.Link>
          </Nav.Item>
        </Nav>
      </div>
      <Routes>
        <Route path="/" element={<Navigate to="list" />} />
        <Route
          path="list"
          element={<TableComponent licitaciones={filteredLicitaciones} />}
        />
        <Route
          path="stats"
          element={
            <StatsLicitaciones
              licitaciones={filteredLicitaciones}
              empresas={empresas}
              valoraciones={valoraciones}
              participaciones={participaciones}
            />
          }
        />
      </Routes>
    </>
  );
};

export default TabLicitaciones;
