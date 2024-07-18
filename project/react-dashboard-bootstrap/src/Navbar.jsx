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
import CustomSwitch from "./CustomSwitch";
import HistoryEduIcon from "@mui/icons-material/HistoryEdu";
import BusinessIcon from "@mui/icons-material/Business";

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
        <Navbar key={expand} expand={expand} className="bg-body-tertiary mb-3">
          <Container fluid>
            <Navbar.Brand href="#">SmarTender AI</Navbar.Brand>
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
                  className="justify-content-begining flex-grow-1 pe-3"
                  defaultActiveKey={location.pathname}
                  variant={isExpanded ? "tabs" : undefined}
                >
                  {/* <Nav.Link
                    as={Link}
                    to="/home"
                    active={location.pathname === "/home"}
                  >
                    <HomeIcon />
                    Home
                  </Nav.Link> */}
                  <Nav.Link
                    as={Link}
                    to="/licitaciones"
                    active={location.pathname.startsWith("/licitaciones")}
                  >
                    <HistoryEduIcon />
                    Licitaciones
                  </Nav.Link>
                  <Nav.Link
                    as={Link}
                    to="/empresas"
                    active={location.pathname.startsWith("/empresas")}
                  >
                    <BusinessIcon />
                    Empresas
                  </Nav.Link>
                  {/* <NavDropdown
                    title="Dropdown"
                    id={`offcanvasNavbarDropdown-expand-${expand}`}
                  >
                    <NavDropdown.Item as={Link} to="#action3">
                      Action
                    </NavDropdown.Item>
                    <NavDropdown.Item as={Link} to="#action4">
                      Another action
                    </NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item as={Link} to="#action5">
                      Something else here
                    </NavDropdown.Item>
                  </NavDropdown> */}
                </Nav>

                <CustomSwitch onChange={handleTheme} />
              </Offcanvas.Body>
            </Navbar.Offcanvas>
          </Container>
        </Navbar>
      ))}
    </>
  );
};

export default MyNavbar;
