import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import Offcanvas from "react-bootstrap/Offcanvas";
import SearchIcon from "@mui/icons-material/Search";
import HomeIcon from "@mui/icons-material/Home";
import BotonCargarExpedientes from "./CargarExpedientes";
import HistoryEduIcon from "@mui/icons-material/HistoryEdu";
import BusinessIcon from "@mui/icons-material/Business";
import "./NavbarStyle.css";

const MyNavbar = ({ toggleTheme }) => {
  const [isExpanded, setIsExpanded] = useState(window.innerWidth >= 768);
  const location = useLocation();

  const handleTheme = () => {
    toggleTheme();
  };

  useEffect(() => {
    const handleResize = () => {
      setIsExpanded(window.innerWidth >= 768); // "md" breakpoint is 768px
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <>
      {["md"].map((expand) => (
        <Navbar key={expand} expand={expand} className="nav-main">
          <Container fluid>
            <Navbar.Brand href="#" className="pb-2 ms-2 pe-3 nav-brand">
              SmarTender AI
            </Navbar.Brand>
            <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-${expand}`} />
            <Navbar.Offcanvas
              id={`offcanvasNavbar-expand-${expand}`}
              aria-labelledby={`offcanvasNavbarLabel-expand-${expand}`}
              placement="end"
            >
              <Offcanvas.Header closeButton>
                <Offcanvas.Title id={`offcanvasNavbarLabel-expand-${expand}`}>
                  Offcanvas
                </Offcanvas.Title>
              </Offcanvas.Header>
              <Offcanvas.Body>
                <Nav
                  className="justify-content-begining flex-grow-1 "
                  defaultActiveKey={location.pathname}
                  variant={isExpanded ? "tabs" : undefined}
                >
                  <Nav.Link
                    as={Link}
                    to="/licitaciones"
                    active={location.pathname.startsWith("/licitaciones")}
                    className="nav-tab-main"
                  >
                    <HistoryEduIcon />
                    Licitaciones
                  </Nav.Link>
                  <Nav.Link
                    as={Link}
                    to="/empresas"
                    active={location.pathname.startsWith("/empresas")}
                    className="nav-tab-main"
                  >
                    <BusinessIcon />
                    Empresas
                  </Nav.Link>
                </Nav>

                <BotonCargarExpedientes />
              </Offcanvas.Body>
            </Navbar.Offcanvas>
          </Container>
        </Navbar>
      ))}
    </>
  );
};

export default MyNavbar;
