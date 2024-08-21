import React, { useState, useEffect } from "react";
import { Button, Spinner, Alert } from "react-bootstrap";

const BotonCargarExpedientes = ({ onChange }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseData, setResponseData] = useState(null);

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
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Button onClick={handleButtonClick} disabled={loading} variant="primary">
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
      {error && (
        <Alert variant="danger" className="mt-3">
          Error: {error}
        </Alert>
      )}
      {responseData && (
        <div className="mt-3">
          <h3>Respuesta:</h3>
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default BotonCargarExpedientes;
