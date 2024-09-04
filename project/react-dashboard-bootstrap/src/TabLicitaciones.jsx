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
import { saveAs } from "file-saver";
import Papa from "papaparse";
import ExcelJS from "exceljs";
import "./TabLicitacionesStyle.css";
const TabLicitaciones = ({ valoraciones, participaciones, empresas }) => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState(null);
  const [licitaciones, setLicitaciones] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [cpvLicitacion, setCpvLicitacion] = useState([]);
  const [visibleColumns, setVisibleColumns] = useState(
    JSON.parse(localStorage.getItem("visibleColumns")) || [
      "EXPEDIENTE",
      "OBJETO",
      "PLAZO_PRESENTACION",
      "DURACION",
      "PROCEDIMIENTO",
      "TRAMITACION",
      "IMPORTE",
      "ADJUDICATARIO",
      "LUGAR",
      "UNIDAD",
      "NUM_OFERTAS",
      "CRITERIOS",
      "OFERTA_ADJ",
    ]
  );
  useEffect(() => {
    localStorage.setItem("visibleColumns", JSON.stringify(visibleColumns));
  }, [visibleColumns]);
  useEffect(() => {
    // Fetch data from licitaciones endpoint
    fetch("http://localhost:8000/api/licitaciones/")
      .then((response) => response.json())
      .then((data) => {
        setLicitaciones(data);

        // Fetch data from cpvlicitacion endpoint after the first fetch completes
        return fetch("http://localhost:8000/api/cpvlicitacion/");
      })
      .then((response) => response.json())
      .then((data) => {
        setCpvLicitacion(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const getCpvCodesForLicitacion = (id_licitacion) => {
    return cpvLicitacion
      .filter((item) => item.id_licitacion === id_licitacion)
      .map((item) => item.id_cpv.id_cpv);
  };

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
        licitacion.tramitacion &&
        filters.tipoTramitacion != licitacion.tramitacion.id_tramitacion
      ) {
        return false;
      }
      if (
        filters.codigoCPV &&
        filters.codigoCPV.length > 0 &&
        !filters.codigoCPV.some((cpv) =>
          getCpvCodesForLicitacion(licitacion.id_licitacion).includes(
            cpv.id_cpv
          )
        )
      ) {
        return false;
      }
    }

    return true;
  };

  const filteredLicitaciones = licitaciones.filter(
    (licitacion) =>
      (licitacion.objeto
        .toLowerCase()
        .includes(searchQuery.toLowerCase().trim()) ||
        licitacion.lugar_ejecucion
          .toLowerCase()
          .includes(searchQuery.toLowerCase().trim()) ||
        licitacion.num_expediente
          .toLowerCase()
          .includes(searchQuery.toLowerCase().trim())) &&
      checkFiltros(licitacion)
  );

  return (
    <>
      <div className="">
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
              className="licitaciones-tab"
            >
              <FormatListBulletedIcon /> Lista
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              as={Link}
              to="stats"
              active={location.pathname === "/licitaciones/stats"}
              className="licitaciones-tab"
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
          element={
            <TableComponent
              licitaciones={filteredLicitaciones}
              participaciones={participaciones}
              valoraciones={valoraciones}
              visibleColumns={visibleColumns}
              setVisibleColumns={setVisibleColumns}
              empresas={empresas}
              filters={filters}
              query={searchQuery}
            />
          }
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
