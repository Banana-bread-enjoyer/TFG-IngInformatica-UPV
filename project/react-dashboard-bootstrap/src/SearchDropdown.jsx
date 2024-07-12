import React, { useState, useEffect } from "react";
import { Form } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";
import "react-bootstrap-typeahead/css/Typeahead.css";
import "./SearchDropdown.css";

const SearchDropdown = () => {
  const [multiSelections, setMultiSelections] = useState([]);
  const [options, setOptions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/codigoscpv/");
        const data = await response.json();
        setOptions(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  // Custom filter function
  const filterBy = (option, props) => {
    const { num_cpv, descripcion } = option;
    const input = props.text.toLowerCase();
    return (
      num_cpv.toLowerCase().includes(input) ||
      descripcion.toLowerCase().includes(input)
    );
  };

  return (
    <>
      <Form.Group className="row mt-3">
        <Form.Label>Código CPV</Form.Label>
        <Typeahead
          id="basic-typeahead-multiple"
          labelKey={(option) => `${option.num_cpv} - ${option.descripcion}`}
          multiple
          onChange={setMultiSelections}
          options={options}
          placeholder="Elegir códigos CPV"
          selected={multiSelections}
          className="custom-typeahead"
          filterBy={filterBy} // Custom filter function
        />
      </Form.Group>
    </>
  );
};

export default SearchDropdown;
