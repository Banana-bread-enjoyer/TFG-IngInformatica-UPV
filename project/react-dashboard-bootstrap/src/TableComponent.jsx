import React from "react";
import { Link } from "react-router-dom";
import UnfoldMoreOutlinedIcon from "@mui/icons-material/UnfoldMoreOutlined";
import KeyboardArrowUpOutlinedIcon from "@mui/icons-material/KeyboardArrowUpOutlined";
import KeyboardArrowDownOutlinedIcon from "@mui/icons-material/KeyboardArrowDownOutlined";
import "./CustomTable.css";
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

const TableComponent = ({ licitaciones }) => {
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
              "dd/MM/yyyy",
              new Date(),
              { locale: es }
            );
            const dateB = parse(
              b.plazo_presentacion,
              "dd/MM/yyyy",
              new Date(),
              { locale: es }
            );
            return compareAsc(dateA, dateB);
          }),
        PROCEDIMIENTO: (array) =>
          array.sort((a, b) =>
            a.procedimiento.nombre_procedimiento.localeCompare(
              b.procedimiento.nombre_procedimiento
            )
          ),
        TRAMITACION: (array) =>
          array.sort((a, b) =>
            a.tramitacion.nombre_tramitacion.localeCompare(
              b.tramitacion.nombre_tramitacion
            )
          ),
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
          array.sort((a, b) =>
            a.adjudicatario.nombre_empresa.localeCompare(
              b.adjudicatario.nombre_empresa
            )
          ),
        ESTADO: (array) =>
          array.sort((a, b) => a.estado.estado.localeCompare(b.estado.estado)),
      },
    }
  );

  function onSortChange(action, state) {
    console.log(action, state);
  }

  return (
    <Table data={{ nodes: licitaciones }} sort={sort}>
      {(tableList) => (
        <>
          <Header>
            <HeaderRow>
              <HeaderCellSort sortKey="EXPEDIENTE">Expediente</HeaderCellSort>
              <HeaderCellSort sortKey="OBJETO">
                Objeto del Contrato
              </HeaderCellSort>
              <HeaderCellSort sortKey="ESTADO">Estado</HeaderCellSort>
              <HeaderCellSort sortKey="PLAZO_PRESENTACION">
                <div style={{ whiteSpace: "normal" }}>
                  Plazo de Presentación
                </div>
              </HeaderCellSort>
              <HeaderCellSort sortKey="PROCEDIMIENTO">
                <div style={{ whiteSpace: "normal" }}>
                  Tipo de Procedimiento
                </div>
              </HeaderCellSort>
              <HeaderCellSort sortKey="TRAMITACION">
                Tipo de Tramitación
              </HeaderCellSort>
              <HeaderCellSort sortKey="IMPORTE">Importe</HeaderCellSort>
              <HeaderCellSort sortKey="ADJUDICATARIO">
                <div style={{ whiteSpace: "normal" }}>
                  Empresa Adjudicataria
                </div>
              </HeaderCellSort>
              <HeaderCellSort sortKey="LUGAR">
                <div style={{ whiteSpace: "normal" }}>Lugar de Ejecución</div>
              </HeaderCellSort>
              <HeaderCellSort sortKey="UNIDAD">
                <div style={{ whiteSpace: "normal" }}>Unidad Encargada</div>
              </HeaderCellSort>
            </HeaderRow>
          </Header>

          <Body>
            {tableList.map((licitacion) => (
              <Row item={licitacion} key={licitacion.id_licitacion}>
                <Cell style={{ width: "400px" }} className="cellStyle">
                  <Link
                    to={`/licitaciones/list/expediente/${licitacion.id_licitacion}`}
                  >
                    {licitacion.num_expediente}
                  </Link>
                </Cell>
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {licitacion.objeto}
                  </div>
                </Cell>
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {licitacion.estado.estado}
                  </div>
                </Cell>
                <Cell className="cellStyle">
                  {licitacion.plazo_presentacion}
                </Cell>
                <Cell className="cellStyle">
                  {licitacion.procedimiento.nombre_procedimiento}
                </Cell>
                <Cell className="cellStyle">
                  {licitacion.tramitacion.nombre_tramitacion}
                </Cell>
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
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {licitacion.adjudicatario.nombre_empresa}
                  </div>
                </Cell>
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {licitacion.lugar_ejecucion}
                  </div>
                </Cell>
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {licitacion.unidad_encargada}
                  </div>
                </Cell>
              </Row>
            ))}
          </Body>
        </>
      )}
    </Table>
  );
};

export default TableComponent;
