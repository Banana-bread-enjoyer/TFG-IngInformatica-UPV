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

const StatsEmpresas = ({
  licitaciones,
  valoraciones,
  participaciones,
  empresas,
}) => {
  const [empresaData, setEmpresaData] = useState([]);
  const [sortBy, setSortBy] = useState("participacionesCount");
  const [sortOrder, setSortOrder] = useState("desc");
  const [pymeStats, setPymeStats] = useState({});

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
          <ResponsiveContainer width={400} height={400}>
            <PieChart>
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
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default StatsEmpresas;
