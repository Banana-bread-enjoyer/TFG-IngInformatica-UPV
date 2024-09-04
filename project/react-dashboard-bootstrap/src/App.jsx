import React, { useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "bootstrap/dist/css/bootstrap.min.css";
import MyNavbar from "./Navbar.jsx";
import { Container, Button } from "react-bootstrap";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import EqualizerIcon from "@mui/icons-material/Equalizer";
import TableComponent from "./TableComponent.jsx";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";
import SearchBar from "./SearchBar.jsx";
import Nav from "react-bootstrap/Nav";
import TabLicitaciones from "./TabLicitaciones.jsx";
import ExpedienteDetails from "./ExpedienteDetails";
import { fetchItems } from "./services/api";
import LicitacionesList from "./Test.jsx";
import TabEmpresas from "./TabEmpresas.jsx";
function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [participaciones, setParticipaciones] = useState(null);
  const [valoraciones, setValoraciones] = useState(null);
  const [empresas, setEmpresas] = useState(null);
  const toggleTheme = () => {
    setDarkMode(!darkMode);
    const htmlElement = document.querySelector("html");
    htmlElement.setAttribute("data-bs-theme", darkMode ? "dark" : "light");
  };
  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = [
          "http://localhost:8000/api/empresas/",
          "http://localhost:8000/api/participaciones/",
          "http://localhost:8000/api/valoraciones/",
        ];
        const responses = await Promise.all(urls.map((url) => fetch(url)));
        const data = await Promise.all(
          responses.map((response) => response.json())
        );
        setEmpresas(data[0]);
        setParticipaciones(data[1]);
        setValoraciones(data[2]);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);
  if (!empresas || !participaciones || !valoraciones) {
    return <div>Loading...</div>;
  }

  return (
    <div className={`App ${darkMode ? "theme-dark" : "theme-light"}`}>
      <Router>
        <MyNavbar toggleTheme={toggleTheme} />

        {/* <LicitacionesList></LicitacionesList> */}
        <Routes>
          <Route path="/home" element={<div></div>} />
          <Route path="/" element={<Navigate to="/licitaciones" />} />
          <Route
            path="/licitaciones/*"
            element={
              <TabLicitaciones
                empresas={empresas}
                valoraciones={valoraciones}
                participaciones={participaciones}
              />
            }
          />
          <Route
            path="/empresas/*"
            element={
              <TabEmpresas
                empresas={empresas}
                valoraciones={valoraciones}
                participaciones={participaciones}
              />
            }
          />
          <Route
            path="/licitaciones/list/expediente/:expedienteId/*"
            element={
              <ExpedienteDetails
                empresas={empresas}
                valoraciones={valoraciones}
                participaciones={participaciones}
              />
            }
          />
          {/* Add other routes as needed */}
        </Routes>
      </Router>
    </div>
  );
}

export default App;
