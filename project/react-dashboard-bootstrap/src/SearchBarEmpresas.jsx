import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import SearchIcon from "@mui/icons-material/Search";
import "bootstrap/dist/css/bootstrap.min.css";
import TuneIcon from "@mui/icons-material/Tune";
import "./SearchBar.css";
import Dropdown from "react-bootstrap/Dropdown";
import SearchDropdown from "./SearchDropdown";
import "react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css";
import RangeSlider from "react-bootstrap-range-slider";
/* import DropdownFilterEmpresa from "./DropdownFilterEmpresa"; */
const SearchBarEmpresas = ({ setSearchQuery, applyFilters }) => {
  const [value, setValue] = useState(1000000);
  const [searchValue, setSearchValue] = useState("");

  // Handle search input change
  const handleSearchChange = (event) => {
    setSearchValue(event.target.value);
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent default form submission
    setSearchQuery(searchValue); // Update search query
  };

  const handleFilterChange = (filters) => {
    applyFilters(filters);
  };
  return (
    <Form className="d-flex pt-3" onSubmit={handleSubmit}>
      <Button variant="success" className="searchButton ms-2" type="submit">
        <SearchIcon />
      </Button>
      <Form.Control
        type="search"
        placeholder="Search"
        className="searchBar me-2 ms-1"
        aria-label="Search"
        value={searchValue}
        onChange={handleSearchChange}
      />
      {/* <DropdownFilterEmpresa
        onFilterChange={handleFilterChange}
      ></DropdownFilterEmpresa> */}
    </Form>
  );
};

export default SearchBarEmpresas;
