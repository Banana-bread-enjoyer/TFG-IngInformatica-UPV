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
  CartesianGrid,
  Rectangle,
  Label,
} from "recharts";
import { Form, Button } from "react-bootstrap";
import PieChartComponent from "./PieChartComponent";
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
        if (sortBy === "participacionesCount") {
          return sortOrder === "asc"
            ? a.adjudicatarioCount - b.adjudicatarioCount
            : b.adjudicatarioCount - a.adjudicatarioCount;
        }
        return sortOrder === "asc"
          ? a.participacionesCount - b.participacionesCount
          : b.participacionesCount - a.participacionesCount;
      }
      return sortOrder === "asc"
        ? a[sortBy] - b[sortBy]
        : b[sortBy] - a[sortBy];
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
            licitacion.adjudicatario?.id_empresa === empresa.id_empresa
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

      setEmpresaData(sortEmpresaData(aggregatedData));
    }
  }, [empresas, participaciones, licitaciones, sortBy, sortOrder]);

  const aggregateData = () => {
    const procedimientos = {};
    const tramitaciones = {};
    const unidades = {};
    const importe = { total: 0, count: 0 };
    const tiposContrato = {};

    licitaciones.forEach((licitacion) => {
      const procedimiento =
        licitacion.procedimiento?.nombre_procedimiento || "Sin especificar";
      procedimientos[procedimiento] = (procedimientos[procedimiento] || 0) + 1;

      const tramitacion =
        licitacion.tramitacion?.nombre_tramitacion || "Sin especificar";
      tramitaciones[tramitacion] = (tramitaciones[tramitacion] || 0) + 1;

      const tipoContrato =
        licitacion.tipo_contrato?.nombre_tipo_contrato.trim() ||
        "Sin especificar";
      tiposContrato[tipoContrato] = (tiposContrato[tipoContrato] || 0) + 1;

      const unidad = licitacion.unidad_encargada;
      unidades[unidad] = (unidades[unidad] || 0) + 1;

      importe.total += parseFloat(licitacion.importe_sin_impuestos) || 0;
      importe.count += 1;
    });

    return {
      procedimientos,
      tramitaciones,
      unidades,
      importe,
      tiposContrato,
    };
  };

  const { procedimientos, tramitaciones, unidades, importe, tiposContrato } =
    aggregateData();

  const empresaChartData = empresaData.map((empresa) => ({
    name: empresa.name,
    value: empresa.participacionesCount,
    adjudicatarioCount: empresa.adjudicatarioCount,
    expulsadaCount: empresa.expulsadaCount,
  }));

  const procedimientoData = Object.keys(procedimientos).map((key) => ({
    name: key,
    value: (procedimientos[key] / licitaciones.length) * 100,
  }));
  const tramitacionData = Object.keys(tramitaciones).map((key) => ({
    name: key,
    value: (tramitaciones[key] / licitaciones.length) * 100,
  }));
  const tiposData = Object.keys(tiposContrato).map((key) => ({
    name: key,
    value: (tiposContrato[key] / licitaciones.length) * 100,
  }));

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

  const getNumberOfParticipations = (idLicitacion) => {
    let numOfertas = 0;
    participaciones.forEach((participacion) => {
      if (participacion.id_licitacion === idLicitacion) {
        numOfertas += 1;
      }
    });
    return numOfertas;
  };

  const ranges = [
    { min: 0, max: 1000000, label: "0 - 1M" },
    { min: 1000000, max: 2000000, label: "1M - 2M" },
    { min: 2000000, max: 3000000, label: "2M - 3M" },
    { min: 3000000, max: 4000000, label: "3M - 4M" },
    { min: 4000000, max: 5000000, label: "4M - 5M" },
    { min: 5000000, max: 6000000, label: "5M - 6M" },
    { min: 6000000, max: 7000000, label: "6M - 7M" },
    { min: 7000000, max: Infinity, label: "7M+" },
  ];

  const calculateParticipationsPerRange = (licitaciones) => {
    const rangeCounts = ranges.map((range) => ({
      range: range.label,
      totalParticipations: 0,
      count: 0,
      averageParticipations: 0,
    }));

    licitaciones.forEach((licitacion) => {
      const contractValue = licitacion.valor_estimado;
      const participations = getNumberOfParticipations(
        licitacion.id_licitacion
      );
      for (let i = 0; i < ranges.length; i++) {
        if (contractValue >= ranges[i].min && contractValue < ranges[i].max) {
          rangeCounts[i].totalParticipations += participations;
          rangeCounts[i].count += 1;
          break;
        }
      }
    });

    rangeCounts.forEach((range) => {
      range.averageParticipations =
        range.count > 0 ? range.totalParticipations / range.count : 0;
    });

    return rangeCounts;
  };
  const bajaAdjudicatario = (licitacion) => {
    const importe = licitacion.importe_sin_impuestos;
    const adjudicatarioParticipacion = participaciones.find(
      (participacion) =>
        participacion.id_licitacion == licitacion.id_licitacion &&
        participacion.id_empresa == licitacion.adjudicatario.id_empresa
    );
    if (adjudicatarioParticipacion == null) {
      return null;
    }
    const baja =
      ((importe - adjudicatarioParticipacion.importe_ofertado_sin_iva) /
        importe) *
      100;

    return baja;
  };
  const bajasPorRango = (licitaciones) => {
    const rangeBajas = ranges.map((range) => ({
      range: range.label,
      totalBajas: 0,
      count: 0,
      bajaMedia: 0,
    }));

    licitaciones.forEach((licitacion) => {
      const contractValue = licitacion.importe_sin_impuestos;
      const baja = bajaAdjudicatario(licitacion);
      for (let i = 0; i < ranges.length; i++) {
        if (contractValue >= ranges[i].min && contractValue < ranges[i].max) {
          rangeBajas[i].totalBajas += baja;
          rangeBajas[i].count += 1;
          break;
        }
      }
    });

    rangeBajas.forEach((range) => {
      range.bajaMedia = range.count > 0 ? range.totalBajas / range.count : 0;
    });

    return rangeBajas;
  };

  const participationsPerRange = calculateParticipationsPerRange(licitaciones);
  const histogramData = [];
  participationsPerRange.forEach((range) => {
    histogramData.push({ name: range.range, ml: range.averageParticipations });
  });
  const bajasPorRangoValor = bajasPorRango(licitaciones);
  const bajasData = [];
  bajasPorRangoValor.forEach((range) => {
    bajasData.push({ name: range.range, mb: range.bajaMedia });
  });
  console.log(bajasData);
  const numCriterios = (idLicitacion) => {
    const participacionesLicit = participaciones.filter(
      (participacion) => participacion.id_licitacion == idLicitacion
    );
    const participacionIds = participacionesLicit.map(
      (participacion) => participacion.id_participacion
    );

    const valoracionesFiltered = valoraciones.filter((valoracion) =>
      participacionIds.includes(valoracion.id_participacion)
    );
    const uniqueCriterios = new Set(
      valoracionesFiltered.map(
        (valoracion) => valoracion.id_criterio.id_criterio
      )
    );
    return uniqueCriterios.size == 1 ? "Único criterio" : "Varios Criterios";
  };
  const criteriosCounts = licitaciones.reduce(
    (acc, licitacion) => {
      const criterio = numCriterios(licitacion.id_licitacion);
      acc[criterio] += 1;
      return acc;
    },
    { "Único criterio": 0, "Varios Criterios": 0 }
  );

  const criteriosData = Object.keys(criteriosCounts).map((key) => ({
    name: key,
    value: (criteriosCounts[key] / licitaciones.length) * 100,
  }));

  return (
    <div className="main-container pe-3 ps-3">
      <div className="row pt-5 mb-5">
        <div className="col importe-box ms-3 me-3">
          <h5>Número de Licitaciones: </h5>
          <h3>{licitaciones.length}</h3>
        </div>
        <div className="col importe-box">
          <h5>Importe Total: </h5>
          <h3>
            {importe.total.toLocaleString("es-ES", {
              style: "currency",
              currency: "EUR",
            })}
          </h3>
        </div>
        <div className="col importe-box ms-3 me-3">
          <h5>Importe Medio: </h5>
          <h3>
            {(importe.total / importe.count).toLocaleString("es-ES", {
              style: "currency",
              currency: "EUR",
            })}
          </h3>
        </div>
      </div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          flexWrap: "wrap",
        }}
      >
        <div className="chart-container">
          <h3>Procedimientos</h3>
          <PieChartComponent data={procedimientoData} colors={COLORS} />
        </div>
        <div className="chart-container">
          <h3>Tramitaciones</h3>
          <PieChartComponent data={tramitacionData} colors={COLORS} />
        </div>
        <div className="chart-container">
          <h3>Tipo de Contrato</h3>
          <PieChartComponent data={tiposData} colors={COLORS} />
        </div>
        <div className="chart-container">
          <h3>Número de Criterios</h3>
          <PieChartComponent data={criteriosData} colors={COLORS} />
        </div>
        <div class="row pe-3">
          <div class="col-md-6 ">
            <ResponsiveContainer
              width="100%"
              height={550}
              aspect={2}
              className="mt-5 chart-with-controls pb-3 pt-3"
            >
              <h4 className="ms-3">
                Número medio de Licitadores por Rango de Importes
              </h4>
              <BarChart
                data={histogramData}
                margin={{
                  top: 5,
                  right: 10,
                  left: 10,
                  bottom: 20,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name">
                  <Label
                    value="Rangos de Importes en Millones de Euros"
                    offset={0}
                    position="bottom"
                  />
                </XAxis>
                <YAxis />
                <Tooltip
                  formatter={(value, name, props) => `${value.toFixed(2)}`}
                />
                <Bar
                  dataKey="ml"
                  fill={COLORS[1]}
                  name={"Número Medio de Licitadores"}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div class="col-md-6">
            <ResponsiveContainer
              width="100%"
              height={550}
              aspect={2}
              className="mt-5  chart-with-controls pb-3 pt-3"
            >
              <h4 className="ms-3">
                Porcentaje medio de Baja de Adjudicatarios por Rango de Importes
              </h4>
              <BarChart
                data={bajasData}
                margin={{
                  top: 5,
                  right: 10,
                  left: 10,
                  bottom: 20,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name">
                  <Label
                    value="Rangos de Importes en Millones de Euros"
                    offset={0}
                    position="bottom"
                  />
                </XAxis>
                <YAxis />
                <Tooltip
                  formatter={(value, name, props) => `${value.toFixed(2)}%`}
                />

                <Bar
                  dataKey="mb"
                  fill={COLORS[2]}
                  name={"Valor Medio de la Baja del Adjudicatario"}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <ResponsiveContainer
          width="100%"
          height={empresaChartData.length * 47}
          className="mt-5 ms-3 me-3 chart-with-controls pt-3 pb-3 ps-3 pe-3"
          minHeight={"1050px"}
        >
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h3 className="mb-0">Top 20 Empresas</h3>
            <Form className="d-flex align-items-center">
              <Form.Label className="me-2">Ordenar Por:</Form.Label>
              <Form.Select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="me-2"
                style={{ width: "200px" }}
              >
                <option value="participacionesCount">Participaciones</option>
                <option value="adjudicatarioCount">Adjudicaciones</option>
                <option value="expulsadaCount">Exclusiones</option>
              </Form.Select>
              <Button
                variant="primary"
                onClick={() =>
                  setSortOrder(sortOrder === "asc" ? "desc" : "asc")
                }
              >
                {sortOrder === "asc" ? "Descendente" : "Ascendente"}
              </Button>
            </Form>
          </div>

          <BarChart
            layout="vertical"
            data={empresaChartData}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <XAxis type="number" orientation="top" />
            <YAxis dataKey="name" type="category" width={400} />
            <Tooltip />
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
