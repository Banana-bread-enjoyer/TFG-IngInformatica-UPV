import React, { useEffect, useState } from "react";
import { Link, Routes, Route, useLocation, Navigate } from "react-router-dom";
import { Nav } from "react-bootstrap";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import EqualizerIcon from "@mui/icons-material/Equalizer";
import StatsEmpresas from "./StatsEmpresas.jsx";
import SearchBarEmpresas from "./SearchBarEmpresas.jsx";
import { parse, compareAsc } from "date-fns";
import { es } from "date-fns/locale";
import TableEmpresas from "./TableEmpresas.jsx";
const TabEmpresas = ({ valoraciones, participaciones, empresas }) => {
  const location = useLocation();
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState(null);

  const applyFilters = (newFilters) => {
    setFilters(newFilters);
  };

  const checkFiltros = (empresa) => {
    return true;
  };

  const filteredEmpresas = empresas.filter(
    (empresa) =>
      Object.values(empresa).some(
        (value) =>
          typeof value === "string" &&
          value.toLowerCase().includes(searchQuery.toLowerCase())
      ) && checkFiltros(empresa)
  );

  return (
    <>
      <div className="mb-3">
        <SearchBarEmpresas
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
              active={location.pathname === "/empresas/list"}
            >
              <FormatListBulletedIcon /> Lista
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              as={Link}
              to="stats"
              active={location.pathname === "/empresas/stats"}
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
          element={<TableEmpresas empresas={filteredEmpresas} />}
        />
        <Route
          path="stats"
          element={
            <StatsEmpresas
              empresas={empresas}
              participaciones={participaciones}
            />
          }
        />
      </Routes>
    </>
  );
};

export default TabEmpresas;
