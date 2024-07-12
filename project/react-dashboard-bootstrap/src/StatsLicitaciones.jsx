import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
  ResponsiveContainer,
} from "recharts";

const StatsComponent = ({
  licitaciones,
  valoraciones,
  participaciones,
  empresas,
}) => {
  const [empresaData, setEmpresaData] = useState([]);
  const [sortBy, setSortBy] = useState("participacionesCount");
  const [sortOrder, setSortOrder] = useState("desc");

  const sortEmpresaData = (data) => {
    const sortedData = [...data];
    sortedData.sort((a, b) => {
      if (a[sortBy] === b[sortBy]) {
        // Tie-breaking criteria, change 'adjudicatarioCount' to any desired field
        if (sortBy == "participacionesCount") {
          return sortOrder === "asc"
            ? a.adjudicatarioCount - b.adjudicatarioCount
            : b.adjudicatarioCount - a.adjudicatarioCount;
        }
        return sortOrder === "asc"
          ? a.participacionesCount - b.participacionesCount
          : b.participacionesCount - a.participacionesCount;
      }

      if (sortOrder === "asc") {
        return a[sortBy] - b[sortBy];
      } else {
        return b[sortBy] - a[sortBy];
      }
    });
    return sortedData.slice(0, 20);
  };

  useEffect(() => {
    if (empresas.length > 0 && participaciones.length > 0) {
      const aggregatedData = empresas.map((empresa) => {
        const participacionesCount = participaciones.filter(
          (participacion) =>
            participacion.id_empresa === empresa.id_empresa &&
            licitaciones.some(
              (licitacion) =>
                licitacion.id_licitacion === participacion.id_licitacion
            )
        ).length;
        const adjudicatarioCount = licitaciones.filter(
          (licitacion) =>
            licitacion.adjudicatario.id_empresa === empresa.id_empresa
        ).length;
        const expulsadaCount = participaciones.filter(
          (participacion) =>
            participacion.excluida === true &&
            participacion.id_empresa === empresa.id_empresa &&
            licitaciones.some(
              (licitacion) =>
                licitacion.id_licitacion === participacion.id_licitacion
            )
        ).length;
        return {
          id: empresa.id_empresa,
          name: empresa.nombre_empresa,
          participacionesCount,
          adjudicatarioCount,
          expulsadaCount,
        };
      });
      /* aggregatedData.sort(
        (a, b) => b.participacionesCount - a.participacionesCount
      );
      const top20Empresas = aggregatedData.slice(0, 20); */
      setEmpresaData(sortEmpresaData(aggregatedData));
    }
  }, [empresas, participaciones, licitaciones, sortBy, sortOrder]); // Specify dependencies here

  // Helper function to aggregate data
  const aggregateData = () => {
    const estados = {};
    const procedimientos = {};
    const tramitaciones = {};
    const unidades = {};
    const importe = { total: 0, count: 0 };
    const tiposContrato = {};

    licitaciones.forEach((licitacion) => {
      // Aggregate estados
      const estado = licitacion.estado.estado;
      estados[estado] = (estados[estado] || 0) + 1;

      // Aggregate procedimientos
      const procedimiento = licitacion.procedimiento.nombre_procedimiento;
      procedimientos[procedimiento] = (procedimientos[procedimiento] || 0) + 1;

      // Aggregate tramitaciones
      const tramitacion = licitacion.tramitacion.nombre_tramitacion;
      tramitaciones[tramitacion] = (tramitaciones[tramitacion] || 0) + 1;
      // Aggregate tipo contrato
      const tipoContrato = licitacion.tipo_contrato.nombre_tipo_contrato.trim();
      tiposContrato[tipoContrato] = (tiposContrato[tipoContrato] || 0) + 1;
      // Aggregate unidades
      const unidad = licitacion.unidad_encargada;
      unidades[unidad] = (unidades[unidad] || 0) + 1;

      // Aggregate importe
      importe.total += parseFloat(licitacion.importe_sin_impuestos) || 0;
      importe.count += 1;
    });

    return {
      estados,
      procedimientos,
      tramitaciones,
      unidades,
      importe,
      tiposContrato,
    };
  };

  const {
    estados,
    procedimientos,
    tramitaciones,
    unidades,
    importe,
    tiposContrato,
  } = aggregateData();
  // Prepare data for BarChart
  const empresaChartData = empresaData.map((empresa) => ({
    name: empresa.name,
    value: empresa.participacionesCount,
    adjudicatarioCount: empresa.adjudicatarioCount,
    expulsadaCount: empresa.expulsadaCount,
  }));
  // Prepare data for charts
  const estadoData = Object.keys(estados).map((key) => ({
    name: key,
    value: estados[key],
  }));
  const procedimientoData = Object.keys(procedimientos).map((key) => ({
    name: key,
    value: procedimientos[key],
  }));
  const tramitacionData = Object.keys(tramitaciones).map((key) => ({
    name: key,
    value: tramitaciones[key],
  }));
  const unidadData = Object.keys(unidades).map((key) => ({
    name: key,
    value: unidades[key],
  }));
  const tiposData = Object.keys(tiposContrato).map((key) => ({
    name: key,
    value: tiposContrato[key],
  }));

  const COLORS = [
    "#d0848d",
    "#82ca9d",
    "#ffc658",
    "#84d8c6",
    "#c684d8",
    "#8884d8",
    "#d8a384",
    "#B6E2DD",
    "#C8DDBB",
    "#E9E5AF",
    "#FBDF9D",
    "#FBC99D",
    "#FBB39D",
    "#FBA09D",
    "#ffd5c2",
    "#588b8b",
    "#ff6f59",
    "#b01041",
    "#223f5a",
  ];
  const tooltipStyles = {
    backgroundColor: "#333",
    color: "#fff",
    border: "1px solid #ccc",
    padding: "10px",
    borderRadius: "5px",
  };
  return (
    <div>
      <div style={{ marginTop: "20px", textAlign: "center" }}>
        <h3>
          Importe Total:{" "}
          {importe.total.toLocaleString("es-ES", {
            style: "currency",
            currency: "EUR",
          })}
        </h3>
        <h4>
          Importe Medio:{" "}
          {(importe.total / importe.count).toLocaleString("es-ES", {
            style: "currency",
            currency: "EUR",
          })}
        </h4>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          flexWrap: "wrap",
        }}
      >
        <div>
          <h3>Estados</h3>
          <PieChart width={400} height={400}>
            <Pie
              data={estadoData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={150}
              fill="#8884d8"
              label
            >
              {estadoData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
        <div>
          <h3>Procedimientos</h3>
          <PieChart width={400} height={400}>
            <Pie
              data={procedimientoData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={150}
              fill="#8884d8"
              label
            >
              {procedimientoData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
        <div>
          <h3>Tramitaciones</h3>
          <PieChart width={400} height={400}>
            <Pie
              data={tramitacionData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={150}
              fill="#8884d8"
              label
            >
              {tramitacionData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
        <div>
          <h3>Tipo de Contrato</h3>
          <PieChart width={400} height={400}>
            <Pie
              data={tiposData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={150}
              fill="#8884d8"
              label
            >
              {tiposData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
        <div style={{ marginBottom: "10px" }}>
          <label>Ordenar Por:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            style={{ marginLeft: "10px" }}
          >
            <option value="participacionesCount">Participaciones</option>
            <option value="adjudicatarioCount">Adjudicaciones</option>
            <option value="expulsadaCount">Exclusiones</option>
          </select>
          <button
            onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
          >
            {sortOrder === "asc" ? "Descendente" : "Ascendente"}
          </button>
        </div>
        <ResponsiveContainer
          width="100%"
          height={empresaChartData.length * 50 + 100}
        >
          <h3>Top Empresas</h3>
          <BarChart
            layout="vertical" // Change layout to horizontal
            data={empresaChartData}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <XAxis type="number" />
            <YAxis dataKey="name" type="category" width={400} />
            <Tooltip contentStyle={tooltipStyles} />
            <Legend />
            <Bar dataKey="value" name={"Participaciones"} fill={COLORS[0]} />
            <Bar
              dataKey="adjudicatarioCount"
              name={"Adjudicaciones"}
              fill={COLORS[1]}
            />
            <Bar
              dataKey="expulsadaCount"
              name={"Exclusiones"}
              fill={COLORS[2]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default StatsComponent;
