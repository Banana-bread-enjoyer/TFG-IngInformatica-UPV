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
  ComposedChart,
  CartesianGrid,
  Line,
} from "recharts";
import Table from "react-bootstrap/Table";
import { parse, compareAsc } from "date-fns";
import { es } from "date-fns/locale";

const StatsEmpresas = ({ valoraciones, participaciones, empresas }) => {
  const [empresaData, setEmpresaData] = useState([]);
  const [sortBy, setSortBy] = useState("participacionesCount");
  const [sortOrder, setSortOrder] = useState("desc");
  const [pymeStats, setPymeStats] = useState({});
  const [licitaciones, setLicitaciones] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/licitaciones/")
      .then((response) => response.json())
      .then((data) => {
        setLicitaciones(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);
  useEffect(() => {
    // Calculate PYME stats
    const calculatePymeStats = () => {
      const pymeCount = empresas.filter(
        (empresa) => empresa.pyme === true
      ).length;
      const noPymeCount = empresas.filter(
        (empresa) => empresa.pyme === false
      ).length;
      const unknownCount = empresas.filter(
        (empresa) => empresa.pyme === null
      ).length;

      return { pymeCount, noPymeCount, unknownCount };
    };

    // Set state with calculated stats
    setPymeStats(calculatePymeStats());
  }, [empresas]);

  // Data for the pie chart
  const pieChartData = [
    { name: "Sí", value: pymeStats.pymeCount || 0 },
    { name: "No", value: pymeStats.noPymeCount || 0 },
    { name: "Desconocido", value: pymeStats.unknownCount || 0 },
  ];
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

  // Helper function to aggregate data

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
  const startYear = 2019;
  const currentYear = new Date().getFullYear() - 1;
  const years = Array.from(
    { length: currentYear - startYear + 1 },
    (_, i) => startYear + i
  );

  const computeMetricsByYear = () => {
    const metricsByYear = years.map((year) => {
      const metrics = empresas.map((empresa) => {
        const participacionesYear = participaciones.filter((p) => {
          const licitacion = licitaciones.find(
            (l) => l.id_licitacion == p.id_licitacion
          );
          return (
            p.id_empresa == empresa.id_empresa &&
            licitacion &&
            new parse(licitacion.plazo_presentacion, "dd/MM/yyyy", new Date(), {
              locale: es,
            }).getFullYear() === year
          );
        });
        const numParticipaciones = participacionesYear.length;

        const numAdjudicaciones = licitaciones.filter(
          (l) =>
            l.adjudicatario.id_empresa == empresa.id_empresa &&
            parse(l.plazo_presentacion, "dd/MM/yyyy", new Date(), {
              locale: es,
            }).getFullYear() == year
        ).length;
        const percentage =
          numParticipaciones > 0
            ? (participacionesYear.reduce((acc, p) => {
                const licitacion = licitaciones.find(
                  (l) => l.id_licitacion === p.id_licitacion
                );
                return (
                  acc +
                  (licitacion.importe_sin_impuestos -
                    p.importe_ofertado_sin_iva) /
                    licitacion.importe_sin_impuestos
                );
              }, 0) /
                numParticipaciones) *
              100
            : 0;
        return {
          name: empresa.nombre_empresa,
          year: year,
          participations: numParticipaciones,
          wins: numAdjudicaciones,
          percentage: percentage.toFixed(2), // Keeping two decimal places for percentage
        };
      });

      return { year, metrics };
    });

    return metricsByYear;
  };

  // Compute the data for the chart
  const metricsByYear = computeMetricsByYear();

  const ranges = [
    { min: 0, max: 100000, label: "0 - 100,000" },
    { min: 100000, max: 500000, label: "100,000 - 500,000" },
    { min: 500000, max: 1000000, label: "500,000 - 1,000,000" },
    { min: 1000000, max: 2000000, label: "1,000,000 - 2,000,000" },
    { min: 2000000, max: 3000000, label: "2,000,000 - 3,000,000" },
    { min: 3000000, max: 4000000, label: "3,000,000 - 4,000,000" },
    { min: 4000000, max: 5000000, label: "4,000,000 - 5,000,000" },
    { min: 5000000, max: 6000000, label: "5,000,000 - 6,000,000" },
    { min: 6000000, max: 7000000, label: "6,000,000 - 7,000,000" },
    { min: 7000000, max: Infinity, label: "7,000,000+" },
  ];
  const computeMetricsByRange = () => {
    const metricsByRange = empresas.map((empresa) => {
      const metrics = ranges.map((range) => {
        const participacionesInRange = participaciones.filter((p) => {
          const licitacion = licitaciones.find(
            (l) => l.id_licitacion === p.id_licitacion
          );
          return (
            p.id_empresa === empresa.id_empresa &&
            licitacion &&
            p.importe_ofertado_sin_iva >= range.min &&
            p.importe_ofertado_sin_iva < range.max
          );
        });

        const numParticipations = participacionesInRange.length;
        const numWins = licitaciones.filter((l) => {
          const participacion = participaciones.find(
            (p) =>
              p.id_licitacion == l.id_licitacion &&
              p.id_empresa == empresa.id_empresa
          );
          return (
            l.adjudicatario.id_empresa == empresa.id_empresa &&
            participacion &&
            participacion.importe_ofertado_sin_iva >= range.min &&
            participacion.importe_ofertado_sin_iva < range.max
          );
        }).length;

        const successPercentage =
          numParticipations > 0 ? (numWins / numParticipations) * 100 : 0;

        return {
          rangeLabel: range.label,
          successPercentage: successPercentage.toFixed(2),
        };
      });

      return {
        empresa: empresa.nombre_empresa,
        metrics,
      };
    });

    return metricsByRange;
  };

  // Example usage
  const metricsByRange = computeMetricsByRange();
  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          flexWrap: "wrap",
        }}
      >
        <div>
          <h3>Empresas PYME</h3>

          <PieChart width={400} height={400}>
            <Pie
              data={pieChartData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={150}
              fill="#8884d8"
              label
            >
              {pieChartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
      </div>
      <div
        className="border ms-3 me-3"
        style={{ overflowX: "scroll", overflowY: "scroll", height: "700px" }}
        width="100%"
      >
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Empresa</th>
              {years.map((year) => (
                <th colSpan={3} key={year}>
                  {year}
                </th>
              ))}
            </tr>
            <tr>
              <th></th>
              {years.map((year) => (
                <>
                  <th key={`${year}-baja`} style={{ fontSize: "12px" }}>
                    Baja Media
                  </th>
                  <th
                    key={`${year}-adjudicaciones`}
                    style={{ fontSize: "12px" }}
                  >
                    Adjudicaciones
                  </th>
                  <th
                    key={`${year}-participaciones`}
                    style={{ fontSize: "12px" }}
                  >
                    Participaciones
                  </th>
                </>
              ))}
            </tr>
          </thead>
          <tbody>
            {empresas.map((empresa) => (
              <tr key={empresa.id_empresa}>
                <td>{empresa.nombre_empresa}</td>
                {years.map((year) => {
                  const metrics = metricsByYear.find(
                    (m) => m.year === year
                  ).metrics;
                  const empresaMetrics = metrics.find(
                    (m) => m.name === empresa.nombre_empresa
                  );

                  return (
                    <React.Fragment key={year}>
                      <td>
                        {empresaMetrics ? empresaMetrics.percentage : "N/A"}
                      </td>
                      <td>{empresaMetrics ? empresaMetrics.wins : "N/A"}</td>
                      <td>
                        {empresaMetrics ? empresaMetrics.participations : "N/A"}
                      </td>
                    </React.Fragment>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
      <div
        className="border ms-3 me-3"
        style={{ overflowX: "scroll", overflowY: "scroll", height: "700px" }}
        width="100%"
      >
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Empresa</th>
              {ranges.map((range) => (
                <th key={range.label}>{range.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {metricsByRange.map((empresaMetrics) => (
              <tr key={empresaMetrics.empresa}>
                <td>{empresaMetrics.empresa}</td>
                {empresaMetrics.metrics.map((metric) => (
                  <td key={metric.rangeLabel}>{metric.successPercentage}%</td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default StatsEmpresas;
