import React, { useState, useEffect } from "react";
import { Button, Spinner, Alert } from "react-bootstrap";

const BotonCargarExpedientes = ({ onChange }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [updateDate, setUpdateDate] = useState(new Date().toLocaleString());

  // Load the date from the backend when the component mounts
  useEffect(() => {
    fetch("http://localhost:8000/api/last-update/")
      .then((response) => response.json())
      .then((data) => {
        setUpdateDate(data.last_update || "No disponible");
      })
      .catch((err) => {
        setError("Error loading date");
        console.error(err);
      });
  }, []);
  const handleButtonClick = async () => {
    setLoading(true);
    setError(null);
    setResponseData(null);

    try {
      const response = await fetch(
        "http://localhost:8000/api/run-script-extraccion/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResponseData(data);
      const newDate = new Date().toLocaleString();
      console.log(newDate);
      setUpdateDate(newDate);
      fetch("http://localhost:8000/api/last-update/set/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ last_update: newDate }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .catch((err) => {
          setLoading(false);
          setError("Error saving date");
          console.error(err);
        });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="d-flex align-items-center pb-2">
        <p className="me-3 mt-2" style={{ color: "white" }}>
          Última actualización: {updateDate}
        </p>
        {error && (
          <Alert variant="danger" className="mt-3 me-3">
            Error: {error}
          </Alert>
        )}
        {responseData && (
          <Alert variant="success" className="mt-3 me-3">
            Expedientes cargados con éxito
          </Alert>
        )}
        <Button
          onClick={handleButtonClick}
          disabled={loading}
          variant="primary"
        >
          {loading ? (
            <div className="d-flex align-items-center">
              <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
              />
              <span className="ms-2">Ejecutando...</span>
            </div>
          ) : (
            "Cargar Nuevos Expedientes"
          )}
        </Button>
      </div>
    </div>
  );
};

export default BotonCargarExpedientes;
