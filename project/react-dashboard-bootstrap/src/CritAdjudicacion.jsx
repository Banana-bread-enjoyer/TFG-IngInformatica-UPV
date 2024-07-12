import React, { useState, useEffect } from "react";
import Table from "react-bootstrap/Table";

const CritAdjudicacion = ({
  licitacion,
  participaciones,
  empresas,
  valoraciones,
}) => {
  const [filteredParticipaciones, setFilteredParticipaciones] = useState([]);
  const [filteredValoraciones, setFilteredValoraciones] = useState([]);
  const [criterios, setCriterios] = useState([]);
  const [error, setError] = useState(null);
  const [statistics, setStatistics] = useState([]);
  const licitacionId = licitacion.id_licitacion;
  useEffect(() => {
    if (licitacion && licitacion.id_licitacion && participaciones.length > 0) {
      const filteredParticipaciones = participaciones.filter(
        (participacion) =>
          participacion.id_licitacion === licitacion.id_licitacion
      );
      setFilteredParticipaciones(filteredParticipaciones);
    }
  }, [licitacion, participaciones]);

  useEffect(() => {
    if (filteredParticipaciones.length > 0 && valoraciones.length > 0) {
      const filteredVals = valoraciones.filter((valoracion) =>
        filteredParticipaciones.some(
          (participacion) =>
            valoracion.id_participacion === participacion.id_participacion
        )
      );
      setFilteredValoraciones(filteredVals);

      const listaCriterios = [
        ...new Map(
          filteredVals.map((item) => [
            item.id_criterio.id_criterio,
            item.id_criterio,
          ])
        ).values(),
      ];
      setCriterios(listaCriterios);
    }
  }, [filteredParticipaciones, valoraciones]);

  useEffect(() => {
    fetch(`http://localhost:8000/api/statistics/${licitacionId}/`)
      .then((response) => response.json())
      .then((data) => setStatistics(data))
      .catch((error) => console.error("Error fetching statistics:", error));
  }, [licitacionId]);

  if (!participaciones) {
    return <div>Loading...</div>;
  }

  // Render error as a string instead of an object
  if (error) {
    return <div>Error: {error.toString()}</div>;
  }

  const getEmpresaName = (idEmpresa) => {
    const empresa = empresas.find((emp) => emp.id_empresa === idEmpresa);
    return empresa ? empresa.nombre_empresa : "Unknown";
  };

  const getPuntuacion = (idParticipacion, idCriterio) => {
    const valoracion = filteredValoraciones.find(
      (val) =>
        val.id_participacion === idParticipacion &&
        val.id_criterio.id_criterio === idCriterio
    );
    return valoracion ? valoracion.puntuacion : "-";
  };

  return (
    <div className="container mt-3">
      <h3>Listado Criterios</h3>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Criterio</th>
            <th>Valor Máximo</th>
            <th>Valor Mínimo</th>
            <th>Media</th>
            <th>Mediana</th>
            <th>Desviación Típica</th>

            <th>Diferencia Primera y Segunda Posición</th>
          </tr>
        </thead>
        <tbody>
          {statistics.map((stat) => (
            <tr key={stat.criterio}>
              <td>{stat.criterio}</td>
              <td>{stat.max}</td>
              <td>{stat.min}</td>
              <td>{stat.average}</td>
              <td>{stat.median}</td>
              <td>{stat.standard_deviation}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      <h3>Valoraciones de las empresas</h3>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Empresa</th>
            <th>Oferta Económica</th>
            {criterios.map((criterio) => (
              <th key={criterio.id_criterio}>{criterio.nombre}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filteredParticipaciones.map((participacion) => (
            <tr key={participacion.id_participacion}>
              <td>{getEmpresaName(participacion.id_empresa)}</td>
              <td>
                {participacion.importe_ofertado_sin_iva
                  ? parseFloat(
                      participacion.importe_ofertado_sin_iva
                    ).toLocaleString("es-ES", {
                      style: "currency",
                      currency: "EUR",
                      minimumFractionDigits: 2,
                    })
                  : "-"}
              </td>
              {criterios.map((criterio) => (
                <td key={criterio.id_criterio}>
                  {getPuntuacion(
                    participacion.id_participacion,
                    criterio.id_criterio
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default CritAdjudicacion;
