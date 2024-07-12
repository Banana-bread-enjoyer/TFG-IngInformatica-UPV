import React, { useEffect, useState } from "react";

const LicitacionesList = () => {
  const [licitaciones, setLicitaciones] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/licitaciones/") // Replace with your Django API URL
      .then((response) => response.json())
      .then((data) => {
        setLicitaciones(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  return (
    <div>
      <h1>List of Licitaciones</h1>
      <ul>
        {licitaciones.map((licitacion) => (
          <li key={licitacion.id_licitacion}>
            <h2>{licitacion.num_expediente}</h2>
            <p>Fecha Adjudicación: {licitacion.fecha_adjudicacion}</p>
            <p>Importe con impuestos: {licitacion.importe_con_impuestos}</p>
            {/* Add more fields as needed */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LicitacionesList;
