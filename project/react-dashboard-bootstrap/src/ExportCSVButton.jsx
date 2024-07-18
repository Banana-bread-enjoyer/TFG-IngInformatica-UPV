import React, { useState } from "react";
import axios from "axios";

const ExportCSV = () => {
  const [loading, setLoading] = useState(false);

  const fetchDataAndExport = async () => {
    setLoading(true);
    try {
      // Fetch data from multiple endpoints
      const urls = [
        "http://localhost:8000/api/empresas/",
        "http://localhost:8000/api/participaciones/",
        "http://localhost:8000/api/valoraciones/",
        "http://localhost:8000/api/licitaciones/",
      ];

      const requests = urls.map((url) => axios.get(url));
      const responses = await Promise.all(requests);

      // Merge the data
      const mergedData = responses.flatMap((response) => response.data);

      // Convert merged data to CSV
      const csvData = convertToCSV(mergedData);
      console.log(csvData);
      // Trigger CSV download
      exportToCSV(csvData);
    } catch (error) {
      console.error("Error fetching data", error);
    } finally {
      setLoading(false);
    }
  };

  const convertToCSV = (array) => {
    if (array.length === 0) {
      return "";
    }
    const keys = Object.keys(array[0]);
    const csvRows = [
      keys.join(","), // header row first
      ...array.map((row) => keys.map((key) => row[key]).join(",")),
    ];
    return csvRows.join("\n");
  };

  const exportToCSV = (csvData) => {
    const blob = new Blob([csvData], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <button onClick={fetchDataAndExport} disabled={loading}>
        {loading ? "Fetching Data..." : "Fetch and Export to CSV"}
      </button>
    </div>
  );
};

export default ExportCSV;
