import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Dropdown from "react-bootstrap/Dropdown";
import TuneIcon from "@mui/icons-material/Tune";
import SearchDropdown from "./SearchDropdown";
import "bootstrap/dist/css/bootstrap.min.css";
import "./SearchBar.css";

const DropdownFilterLicitacion = ({ onFilterChange }) => {
  const [tipoprocedimiento, setTipoprocedimiento] = useState([]);
  const [tipocontrato, setTipocontrato] = useState([]);
  const [tipotramitacion, setTipotramitacion] = useState([]);
  const [filters, setFilters] = useState({
    lugarEjecucion: "",
    importeMax: "",
    importeMin: "",
    unidadEncargada: "",
    plazoPresentacionDesde: "",
    plazoPresentacionHasta: "",
    tipoContrato: "",
    tipoProcedimiento: "",
    tipoTramitacion: "",
    codigoCPV: [],
  });

  const [appliedFilters, setAppliedFilters] = useState({});
  const [selectedItems, setSelectedItems] = useState([]);

  const handleSelectionChange = (selected) => {
    if (selected.length != selectedItems.length) {
      setSelectedItems(selected);
    }
  };
  useEffect(() => {
    if (selectedItems !== filters.codigoCPV) {
      setFilters((prevFilters) => ({
        ...prevFilters,
        codigoCPV: selectedItems,
      }));
    }
  }, [selectedItems]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = [
          "http://localhost:8000/api/tipocontrato/",
          "http://localhost:8000/api/tipoprocedimiento/",
          "http://localhost:8000/api/tipotramitacion/",
        ];
        const responses = await Promise.all(urls.map((url) => fetch(url)));
        const data = await Promise.all(
          responses.map((response) => response.json())
        );
        setTipocontrato(data[0]);
        setTipoprocedimiento(data[1]);
        setTipotramitacion(data[2]);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleFilterChange = (event) => {
    const { id, value } = event.target;

    setFilters({
      ...filters,
      [id]: value,
    });
  };

  const applyFilters = () => {
    setAppliedFilters(filters);
    onFilterChange(filters);
    console.log(filters);
  };

  const handleClearFilters = () => {
    setSelectedItems([]);
    setFilters({
      lugarEjecucion: "",
      importeMax: "",
      importeMin: "",
      unidadEncargada: "",
      plazoPresentacionDesde: "",
      plazoPresentacionHasta: "",
      tipoContrato: "",
      tipoProcedimiento: "",
      tipoTramitacion: "",
      codigoCPV: [],
    });
    setAppliedFilters({});
    onFilterChange({});
  };

  return (
    <Dropdown>
      <Dropdown.Toggle
        className="dropdownButton me-2"
        variant="success"
        id="dropdown-basic"
      >
        <TuneIcon />
      </Dropdown.Toggle>

      <Dropdown.Menu className="ps-3 pe-3 dropdownMenu container">
        <div className="row mt-3">
          <Form.Group controlId="lugarEjecucion" className="col">
            <Form.Label>Lugar de Ejecución</Form.Label>
            <Form.Control
              placeholder="Introducir Ciudad"
              value={filters.lugarEjecucion}
              onChange={handleFilterChange}
            />
          </Form.Group>
          <Form.Group className="col">
            <Form.Label>Importe del Contrato</Form.Label>
            <div className="row">
              <div className="col">
                <Form.Control
                  placeholder="MIN"
                  id="importeMin"
                  value={filters.importeMin}
                  onChange={handleFilterChange}
                />
              </div>
              <div className="col">
                <Form.Control
                  placeholder="MAX"
                  id="importeMax"
                  value={filters.importeMax}
                  onChange={handleFilterChange}
                />
              </div>
            </div>
          </Form.Group>
        </div>
        <div className="row mt-3">
          <Form.Group controlId="unidadEncargada" className="col">
            <Form.Label>Unidad Encargada</Form.Label>
            <Form.Control
              placeholder="Unidad Encargada"
              value={filters.unidadEncargada}
              onChange={handleFilterChange}
            />
          </Form.Group>
          <Form.Group className="col">
            <Form.Label>Plazo de Presentación</Form.Label>
            <div className="row">
              <div className="col">
                <Form.Control
                  type="date"
                  placeholder="Desde"
                  id="plazoPresentacionDesde"
                  value={filters.plazoPresentacionDesde}
                  onChange={handleFilterChange}
                />
              </div>
              <div className="col">
                <Form.Control
                  type="date"
                  placeholder="Hasta"
                  id="plazoPresentacionHasta"
                  value={filters.plazoPresentacionHasta}
                  onChange={handleFilterChange}
                />
              </div>
            </div>
          </Form.Group>
        </div>
        <div className="row mt-3">
          <Form.Group controlId="formContrato" className="col">
            <Form.Label>Tipo de Contrato</Form.Label>
            <Form.Select
              value={filters.tipoContrato}
              onChange={handleFilterChange}
              id="tipoContrato"
            >
              <option value="">Seleccionar Tipo</option>
              {tipocontrato.map((tipocontrato) => (
                <option
                  key={tipocontrato.id_tipo_contrato}
                  value={tipocontrato.id_tipo_contrato}
                >
                  {tipocontrato.nombre_tipo_contrato}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
          <Form.Group controlId="formPresentacion" className="col">
            <Form.Label>Tipo de Procedimiento</Form.Label>
            <Form.Select
              value={filters.tipoProcedimiento}
              onChange={handleFilterChange}
              id="tipoProcedimiento"
            >
              <option value="">Seleccionar Procedimiento</option>
              {tipoprocedimiento.map((tipoprocedimiento) => (
                <option
                  key={tipoprocedimiento.id_procedimiento}
                  value={tipoprocedimiento.id_procedimiento}
                >
                  {tipoprocedimiento.nombre_procedimiento}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
          <Form.Group controlId="formTramitacion" className="col">
            <Form.Label>Tipo de Tramitación</Form.Label>
            <Form.Select
              value={filters.tipoTramitacion}
              onChange={handleFilterChange}
              id="tipoTramitacion"
            >
              <option value="">Seleccionar Tramitación</option>
              {tipotramitacion.map((tipotramitacion) => (
                <option
                  key={tipotramitacion.id_tramitacion}
                  value={tipotramitacion.id_tramitacion}
                >
                  {tipotramitacion.nombre_tramitacion}
                </option>
              ))}
            </Form.Select>
          </Form.Group>
        </div>
        <SearchDropdown
          onSelectionChange={handleSelectionChange}
          selectedItems={selectedItems}
        />
        <div className="row ms-1 mt-3 mb-2">
          <div className="col-2 d-grid gap-2">
            <Button variant="primary" type="submit" onClick={applyFilters}>
              Aplicar
            </Button>
          </div>
          <div className="col-2 d-grid gap-2">
            <Button variant="danger" onClick={handleClearFilters}>
              Limpiar
            </Button>
          </div>
        </div>
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default DropdownFilterLicitacion;
