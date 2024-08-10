import React, { useState, useEffect } from "react";
import { Form } from "react-bootstrap";
import { Typeahead } from "react-bootstrap-typeahead";
import "react-bootstrap-typeahead/css/Typeahead.css";
import "./SearchDropdown.css";

const SearchDropdown = ({ onSelectionChange, selectedItems }) => {
  const [multiSelections, setMultiSelections] = useState([]);
  const [allOptions, setAllOptions] = useState([]);
  const [filteredOptions, setFilteredOptions] = useState([]);
  useEffect(() => {
    // Whenever `selectedItems` is reset, notify the parent component.
    console.log("selected", selectedItems);
    if (selectedItems.length === 0) {
      onSelectionChange([]);
      setMultiSelections([]);
    }
  }, [selectedItems]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/codigoscpv/");
        const data = await response.json();
        setAllOptions(data);
        setFilteredOptions(data); // Initialize filtered options
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    // Update filtered options to exclude selected items
    const filtered = allOptions.filter(
      (option) =>
        !multiSelections.some(
          (selection) => selection.num_cpv === option.num_cpv
        )
    );
    setFilteredOptions(filtered);
  }, [multiSelections, allOptions]);

  // Custom filter function
  const filterBy = (option, props) => {
    const { num_cpv, descripcion } = option;
    const input = props.text.toLowerCase();
    return (
      num_cpv.toLowerCase().includes(input) ||
      descripcion.toLowerCase().includes(input)
    );
  };

  // Handle selection change and notify parent
  const handleSelectionChange = (selected) => {
    setMultiSelections(selected);
    if (onSelectionChange) {
      onSelectionChange(selected);
    }
  };

  return (
    <Form.Group className="row mt-3">
      <Form.Label>Código CPV</Form.Label>
      <Typeahead
        id="basic-typeahead-multiple"
        labelKey={(option) => `${option.num_cpv} - ${option.descripcion}`}
        multiple
        onChange={handleSelectionChange}
        options={filteredOptions} // Use filtered options
        placeholder="Elegir códigos CPV"
        selected={multiSelections}
        className="custom-typeahead"
        filterBy={filterBy}
      />
    </Form.Group>
  );
};

export default SearchDropdown;
