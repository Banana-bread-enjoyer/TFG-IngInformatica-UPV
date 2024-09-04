import React, { useState } from "react";
import { Link } from "react-router-dom";
import UnfoldMoreOutlinedIcon from "@mui/icons-material/UnfoldMoreOutlined";
import KeyboardArrowUpOutlinedIcon from "@mui/icons-material/KeyboardArrowUpOutlined";
import KeyboardArrowDownOutlinedIcon from "@mui/icons-material/KeyboardArrowDownOutlined";
import {
  Table,
  Header,
  HeaderRow,
  Body,
  Row,
  HeaderCell,
  Cell,
} from "@table-library/react-table-library/table";
import {
  useSort,
  HeaderCellSort,
  SortIconPositions,
  SortToggleType,
} from "@table-library/react-table-library/sort";
import { parse, compareAsc } from "date-fns";
import { es } from "date-fns/locale";
import "bootstrap/dist/css/bootstrap.min.css";
import "./TableCustom.css";
import Dropdown from "react-bootstrap/Dropdown";
import Form from "react-bootstrap/Form";
import ExportarExcel from "./ExportarExcel";
const TableComponent = ({
  licitaciones,
  participaciones,
  valoraciones,
  visibleColumns,
  setVisibleColumns,
  empresas,
  filters,
  query,
}) => {
  const columns = [
    { key: "EXPEDIENTE", label: "Expediente" },
    { key: "OBJETO", label: "Objeto del Contrato" },
    { key: "PLAZO_PRESENTACION", label: "Plazo de Presentación" },
    { key: "DURACION", label: "Duración del Contrato" },
    { key: "PROCEDIMIENTO", label: "Tipo de Procedimiento" },
    { key: "TRAMITACION", label: "Tipo de Tramitación" },
    { key: "IMPORTE", label: "Importe" },
    { key: "ADJUDICATARIO", label: "Empresa Adjudicataria" },
    { key: "OFERTA_ADJ", label: "Oferta del Adjudicatario" },
    { key: "NUM_OFERTAS", label: "Número de Ofertas" },
    { key: "CRITERIOS", label: "Criterios de Adjudicación" },
    { key: "LUGAR", label: "Lugar de Ejecución" },
    { key: "UNIDAD", label: "Unidad Encargada" },
  ];

  const sort = useSort(
    licitaciones,
    {
      onChange: onSortChange,
    },
    {
      sortIcon: {
        margin: "0px",
        iconDefault: <UnfoldMoreOutlinedIcon fontSize="small" />,
        iconUp: <KeyboardArrowUpOutlinedIcon fontSize="small" />,
        iconDown: <KeyboardArrowDownOutlinedIcon fontSize="small" />,
      },
      sortFns: {
        EXPEDIENTE: (array) =>
          array.sort((a, b) =>
            a.num_expediente.localeCompare(b.num_expediente)
          ),
        OBJETO: (array) =>
          array.sort((a, b) => a.objeto.localeCompare(b.objeto)),
        PLAZO_PRESENTACION: (array) =>
          array.sort((a, b) => {
            const dateA = parse(
              a.plazo_presentacion,
              "yyyy-mm-dd",
              new Date(),
              { locale: es }
            );
            const dateB = parse(
              b.plazo_presentacion,
              "yyyy-mm-dd",
              new Date(),
              { locale: es }
            );
            return compareAsc(dateA, dateB);
          }),
        PROCEDIMIENTO: (array) =>
          array.sort((a, b) => {
            const procedimientoA = a.procedimiento?.nombre_procedimiento || "";
            const procedimientoB = b.procedimiento?.nombre_procedimiento || "";
            return procedimientoA.localeCompare(procedimientoB);
          }),
        TRAMITACION: (array) =>
          array.sort((a, b) => {
            const tramitacionA = a.tramitacion?.nombre_tramitacion || "";
            const tramitacionB = b.tramitacion?.nombre_tramitacion || "";
            return tramitacionA.localeCompare(tramitacionB);
          }),
        IMPORTE: (array) =>
          array.sort(
            (a, b) => a.importe_sin_impuestos - b.importe_sin_impuestos
          ),
        LUGAR: (array) =>
          array.sort((a, b) =>
            a.lugar_ejecucion.localeCompare(b.lugar_ejecucion)
          ),
        UNIDAD: (array) =>
          array.sort((a, b) =>
            a.unidad_encargada.localeCompare(b.unidad_encargada)
          ),
        ADJUDICATARIO: (array) =>
          array.sort((a, b) => {
            const nameA = a.adjudicatario?.nombre_empresa || "";
            const nameB = b.adjudicatario?.nombre_empresa || "";
            return nameA.localeCompare(nameB);
          }),
        NUM_OFERTAS: (array) =>
          array.sort(
            (a, b) => getOfertas(a.id_licitacion) - getOfertas(b.id_licitacion)
          ),
        CRITERIOS: (array) =>
          array.sort((a, b) =>
            numCriterios(a.id_licitacion).localeCompare(
              numCriterios(b.id_licitacion)
            )
          ),
        OFERTA_ADJ: (array) =>
          array.sort(
            (a, b) => getOfertaAdjudicatario(a) - getOfertaAdjudicatario(b)
          ),
        DURACION: (array) =>
          array.sort((a, b) => {
            const getDurationValue = (duration) => {
              const [num, unit] = duration.split(" ");
              return { num: parseInt(num, 10), unit };
            };

            const unitWeights = {
              "Día(s)": 1,
              "Mes(es)": 2,
              "Año(s)": 3,
            };

            const durationA = getDurationValue(a.plazo_ejecucion);
            const durationB = getDurationValue(b.plazo_ejecucion);

            if (unitWeights[durationA.unit] === unitWeights[durationB.unit]) {
              return durationA.num - durationB.num;
            } else {
              return unitWeights[durationA.unit] - unitWeights[durationB.unit];
            }
          }),
      },
    }
  );

  function onSortChange(action, state) {
    console.log(action, state);
  }

  const handleSelect = (key) => {
    setVisibleColumns((prev) =>
      prev.includes(key) ? prev.filter((col) => col !== key) : [...prev, key]
    );
  };
  const getOfertas = (idLicitacion) => {
    var numOfertas = 0;
    participaciones.map((participacion) => {
      if (participacion.id_licitacion == idLicitacion) {
        numOfertas += 1;
      }
    });
    return numOfertas;
  };
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
  const getOfertaAdjudicatario = (licitacion) => {
    const idLicitacion = licitacion.id_licitacion;
    var idAdjudicatario = null;
    if (licitacion.adjudicatario != null) {
      idAdjudicatario = licitacion.adjudicatario.id_empresa;
    }

    const participacionAdjudicatario = participaciones.find(
      (participacion) =>
        participacion.id_licitacion == idLicitacion &&
        participacion.id_empresa == idAdjudicatario
    );
    if (
      participacionAdjudicatario != null &&
      participacionAdjudicatario.importe_ofertado_sin_iva != null
    ) {
      return participacionAdjudicatario.importe_ofertado_sin_iva;
    } else {
      return null;
    }
  };
  const formatDate = (dateString) => {
    const options = { day: "2-digit", month: "2-digit", year: "numeric" };
    return new Date(dateString).toLocaleDateString("es-ES", options);
  };
  return (
    <div className="main-container ps-3 pe-3">
      <Dropdown>
        <div className="pt-3 pb-3">
          <Dropdown.Toggle
            className="ms-3 me-3"
            variant="success"
            id="dropdown-basic"
          >
            Columnas Visibles
          </Dropdown.Toggle>
          <ExportarExcel
            participaciones={participaciones}
            valoraciones={valoraciones}
            empresas={empresas}
            filteredLicitaciones={licitaciones}
            filters={filters}
            query={query}
          />
        </div>
        <Dropdown.Menu>
          <Form>
            {columns.map(
              (column) =>
                column.key != "EXPEDIENTE" && (
                  <Dropdown.Item
                    key={column.key}
                    onClick={() => handleSelect(column.key)}
                  >
                    <Form.Check
                      type="checkbox"
                      checked={visibleColumns.includes(column.key)}
                      label={column.label}
                      readOnly
                    />
                  </Dropdown.Item>
                )
            )}
          </Form>
        </Dropdown.Menu>
      </Dropdown>
      <div className="table-container">
        <Table data={{ nodes: licitaciones }} sort={sort}>
          {(tableList) => (
            <>
              <Header>
                <HeaderRow>
                  {columns.map((column) => (
                    <HeaderCellSort
                      key={column.key}
                      sortKey={column.key}
                      hide={!visibleColumns.includes(column.key)}
                    >
                      <div style={{ whiteSpace: "normal" }}>{column.label}</div>
                    </HeaderCellSort>
                  ))}
                </HeaderRow>
              </Header>

              <Body>
                {tableList.map((licitacion) => (
                  <Row item={licitacion} key={licitacion.id_licitacion}>
                    {visibleColumns.includes("EXPEDIENTE") && (
                      <Cell className="cellStyle">
                        <Link
                          to={`/licitaciones/list/expediente/${licitacion.id_licitacion}`}
                        >
                          {licitacion.num_expediente}
                        </Link>
                      </Cell>
                    )}
                    {visibleColumns.includes("OBJETO") && (
                      <Cell className="cellStyle">
                        <div style={{ whiteSpace: "normal" }}>
                          {licitacion.objeto}
                        </div>
                      </Cell>
                    )}
                    {visibleColumns.includes("PLAZO_PRESENTACION") && (
                      <Cell className="cellStyle">
                        {formatDate(licitacion.plazo_presentacion)}
                      </Cell>
                    )}
                    {visibleColumns.includes("DURACION") && (
                      <Cell className="cellStyle">
                        {licitacion.plazo_ejecucion}
                      </Cell>
                    )}
                    {visibleColumns.includes("PROCEDIMIENTO") && (
                      <Cell className="cellStyle">
                        {licitacion.procedimiento?.nombre_procedimiento || ""}
                      </Cell>
                    )}
                    {visibleColumns.includes("TRAMITACION") && (
                      <Cell className="cellStyle">
                        {licitacion.tramitacion?.nombre_tramitacion || ""}
                      </Cell>
                    )}
                    {visibleColumns.includes("IMPORTE") && (
                      <Cell className="cellStyle">
                        {licitacion.importe_sin_impuestos
                          ? parseFloat(
                              licitacion.importe_sin_impuestos
                            ).toLocaleString("es-ES", {
                              style: "currency",
                              currency: "EUR",
                              minimumFractionDigits: 2,
                            })
                          : "N/A"}
                      </Cell>
                    )}

                    {visibleColumns.includes("ADJUDICATARIO") && (
                      <Cell className="cellStyle">
                        <div style={{ whiteSpace: "normal" }}>
                          {licitacion.adjudicatario?.nombre_empresa || ""}
                        </div>
                      </Cell>
                    )}
                    {visibleColumns.includes("OFERTA_ADJ") && (
                      <Cell className="cellStyle">
                        {getOfertaAdjudicatario(licitacion)
                          ? parseFloat(
                              getOfertaAdjudicatario(licitacion)
                            ).toLocaleString("es-ES", {
                              style: "currency",
                              currency: "EUR",
                              minimumFractionDigits: 2,
                            })
                          : "N/A"}
                      </Cell>
                    )}
                    {visibleColumns.includes("NUM_OFERTAS") && (
                      <Cell className="cellStyle">
                        {getOfertas(licitacion.id_licitacion)
                          ? getOfertas(licitacion.id_licitacion)
                          : "N/A"}
                      </Cell>
                    )}
                    {visibleColumns.includes("CRITERIOS") && (
                      <Cell className="cellStyle">
                        {numCriterios(licitacion.id_licitacion)
                          ? numCriterios(licitacion.id_licitacion)
                          : "N/A"}
                      </Cell>
                    )}
                    {visibleColumns.includes("LUGAR") && (
                      <Cell className="cellStyle">
                        <div style={{ whiteSpace: "normal" }}>
                          {licitacion.lugar_ejecucion}
                        </div>
                      </Cell>
                    )}
                    {visibleColumns.includes("UNIDAD") && (
                      <Cell className="cellStyle">
                        <div style={{ whiteSpace: "normal" }}>
                          {licitacion.unidad_encargada}
                        </div>
                      </Cell>
                    )}
                  </Row>
                ))}
              </Body>
            </>
          )}
        </Table>
      </div>
    </div>
  );
};

export default TableComponent;
