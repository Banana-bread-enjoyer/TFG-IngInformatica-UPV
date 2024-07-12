import React from "react";
import { FormCheck } from "react-bootstrap";
import "./CustomSwitch.css"; // Make sure to create and import this CSS file

const CustomSwitch = ({ onChange }) => {
  return (
    <FormCheck
      type="switch"
      id="custom-switch"
      label=""
      onChange={onChange}
      className="custom-switch ms-3"
    />
  );
};

export default CustomSwitch;
