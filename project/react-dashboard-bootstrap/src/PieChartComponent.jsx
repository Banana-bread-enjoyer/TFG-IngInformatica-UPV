// PieChartComponent.js
import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const PieChartComponent = ({
  data,
  colors,
  width = 400,
  height = 400,
  outerRadius = 120,
}) => {
  // Custom label renderer to show the percentage and name
  const renderCustomizedLabel = ({ name, value }) => {
    return `${value.toFixed(2)}%`;
  };

  return (
    <div className="pie-chart-wrapper">
      <PieChart width={width} height={height}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={outerRadius}
          fill="#8884d8"
          label={renderCustomizedLabel}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value, name, props) => `${value.toFixed(2)}%`} />
        <Legend />
      </PieChart>
    </div>
  );
};

export default PieChartComponent;
