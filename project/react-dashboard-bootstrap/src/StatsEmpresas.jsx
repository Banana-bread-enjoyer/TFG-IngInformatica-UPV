import React, { useState, useEffect } from "react";
import { Tooltip, PieChart, Pie, Cell, Legend } from "recharts";
import { parse, compareAsc } from "date-fns";
import { es } from "date-fns/locale";
import "./TablasStyle.css";
import EmpresaTableByYear from "./EmpresaTableByYear";
import Table from "react-bootstrap/Table";
import Accordion from "react-bootstrap/Accordion";
import "./StatsStyle.css";
import Spinner from "react-bootstrap/Spinner";
import PieChartComponent from "./PieChartComponent";
const StatsEmpresas = ({ valoraciones, participaciones, empresas }) => {
  const [empresaData, setEmpresaData] = useState([]);
  const [sortBy, setSortBy] = useState("participacionesCount");
  const [sortOrder, setSortOrder] = useState("desc");
  const [pymeStats, setPymeStats] = useState({});
  const [licitaciones, setLicitaciones] = useState([]);
  const [metricsByYear, setMetricsByYear] = useState([]);
  const [metricsByRange, setMetricsByRange] = useState([]);
  const [loading, setLoading] = useState(true); // Loading state
  const [loadingRange, setLoadingRange] = useState(true); // Loading state
  const [pymesData, setPymesData] = useState([]);
  const [loadingPymes, setLoadingPymes] = useState(true); // Loading state

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoadingPymes(true);

        // Fetch aggregated PYME data
        const response = await fetch(
          "http://localhost:8000/api/pymes/aggregate/"
        );
        const data = await response.json();
        setPymesData(data);
      } catch (error) {
        console.error("Error fetching PYME data:", error);
      } finally {
        setLoadingPymes(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Set loading to true before fetching
        setLoading(true);

        const metricsByYearResponse = await fetch(
          "http://localhost:8000/api/metrics-by-year/"
        );
        const metricsByYearData = await metricsByYearResponse.json();
        setMetricsByYear(metricsByYearData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        // Set loading to false after fetching is complete
        setLoading(false);
      }
    };

    fetchData();
  }, []);
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Set loading to true before fetching
        setLoadingRange(true);

        const metricsByRangeResponse = await fetch(
          "http://localhost:8000/api/metrics-by-range/"
        );
        const metricsByRangeData = await metricsByRangeResponse.json();
        setMetricsByRange(metricsByRangeData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        // Set loading to false after fetching is complete
        setLoadingRange(false);
      }
    };

    fetchData();
  }, []);
  // Helper function to aggregate data

  const COLORS = [
    "#22577a",
    "#38a3a5",
    "#57cc99",
    "#84d8c6",
    "#80ed99",
    "#c7f9cc",
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

  const startYear = 2019;
  const currentYear = new Date().getFullYear() - 1;
  const years = Array.from(
    { length: currentYear - startYear + 1 },
    (_, i) => startYear + i
  );

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

  const renderCustomizedLabel = ({ name, value }) => {
    return `${value.toFixed(2)}%`;
  };

  return (
    <div className="main-container pe-3 ps-3">
      <div className="row justify-content-md-center pt-5 mb-5">
        <div className="col-lg-3 ms-3 me-3">
          <div className="row importe-box">
            <h5>Número de Empresas: </h5>
            <h3>{empresas.length}</h3>
          </div>
          <div className="row importe-box">
            <h5>Número de Participaciones: </h5>
            <h3>{participaciones.length}</h3>
          </div>
        </div>
        <div className="col-xl-3 col-md-6 chart-container">
          <h4>Tamaño de empresas</h4>
          {loadingPymes ? (
            <div
              className="d-flex justify-content-center align-items-center"
              style={{ height: "100%" }}
            >
              <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
              </Spinner>
            </div>
          ) : (
            <PieChart width={400} height={400}>
              <Pie
                data={pymesData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                fill="#8884d8"
                label={renderCustomizedLabel}
              >
                {pymesData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value, name, props) => `${value.toFixed(2)}%`}
              />
              <Legend />
            </PieChart>
          )}
        </div>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          flexWrap: "wrap",
        }}
      ></div>
      <Accordion className="ms-3 me-3" defaultActiveKey="0" alwaysOpen>
        <Accordion.Item eventKey="0">
          <Accordion.Header>
            Baja Media, Adjudicaciones y Participaciones de cada Empresa por año
          </Accordion.Header>
          <Accordion.Body>
            <div
              className="border ms-3 me-3"
              style={{
                overflowX: "scroll",
                overflowY: "scroll",
                height: "700px",
              }}
              width="100%"
            >
              {loading ? (
                <div
                  className="d-flex justify-content-center align-items-center"
                  style={{ height: "100%" }}
                >
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                </div>
              ) : (
                <Table striped bordered hover>
                  <thead className="sticky-top">
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
                        <React.Fragment key={`${year}-headers`}>
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
                        </React.Fragment>
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
                                {empresaMetrics
                                  ? empresaMetrics.percentage
                                  : "N/A"}
                                %
                              </td>
                              <td>
                                {empresaMetrics ? empresaMetrics.wins : "N/A"}
                              </td>
                              <td>
                                {empresaMetrics
                                  ? empresaMetrics.participations
                                  : "N/A"}
                              </td>
                            </React.Fragment>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </div>
          </Accordion.Body>
        </Accordion.Item>
        <Accordion.Item eventKey="1">
          <Accordion.Header>
            Porcentaje de éxito de cada empresa por tamaño de contrato
          </Accordion.Header>
          <Accordion.Body>
            <div
              className="border ms-3 me-3"
              style={{
                overflowX: "scroll",
                overflowY: "scroll",
                height: "700px",
              }}
              width="100%"
            >
              {loadingRange ? (
                <div
                  className="d-flex justify-content-center align-items-center"
                  style={{ height: "100%" }}
                >
                  <Spinner animation="border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </Spinner>
                </div>
              ) : (
                <Table striped bordered hover>
                  <thead className="sticky-top">
                    <tr>
                      <th>Empresa</th>
                      <th>Total</th>
                      {ranges.map((range) => (
                        <th key={range.label}>{range.label}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {metricsByRange.map((empresaMetrics) => (
                      <tr key={empresaMetrics.empresa}>
                        <td>{empresaMetrics.empresa}</td>
                        <td>{empresaMetrics.totalSuccessPercentage}%</td>
                        {empresaMetrics.metrics.map((metric) => (
                          <td key={metric.rangeLabel}>
                            {metric.successPercentage}%
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </Table>
              )}
            </div>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </div>
  );
};

export default StatsEmpresas;
