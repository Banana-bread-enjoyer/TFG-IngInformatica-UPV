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
import { useTheme } from "@table-library/react-table-library/theme";

const TableEmpresas = ({ empresas }) => {
  const theme = useTheme({
    Table: `
        --data-table-library_grid-template-columns: 50% auto auto;
      `,
  });
  const sort = useSort(
    empresas,
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
        NOMBRE: (array) =>
          array.sort((a, b) =>
            a.nombre_empresa.localeCompare(b.nombre_empresa)
          ),
        PYME: (array) =>
          array.sort((a, b) => {
            if (a.pyme === null && b.pyme !== null) return 1;
            if (a.pyme !== null && b.pyme === null) return -1;
            if (a.pyme === null && b.pyme === null) return 0;
            return a.pyme.toString().localeCompare(b.pyme.toString());
          }),
        NIF: (array) =>
          array.sort((a, b) => (a.nif || "").localeCompare(b.nif || "")),
      },
    }
  );

  function onSortChange(action, state) {
    console.log(action, state);
  }

  return (
    <Table
      theme={theme}
      data={{ nodes: empresas }}
      sort={sort}
      layout={{ custom: true }}
    >
      {(tableList) => (
        <>
          <Header>
            <HeaderRow>
              <HeaderCellSort sortKey="NOMBRE">Nombre Empresa</HeaderCellSort>
              <HeaderCellSort sortKey="NIF">NIF Empresa</HeaderCellSort>
              <HeaderCellSort sortKey="PYME">¿Es PYME?</HeaderCellSort>
            </HeaderRow>
          </Header>

          <Body>
            {tableList.map((empresa) => (
              <Row item={empresa} key={empresa.id_empresa}>
                <Cell className="cellStyle">
                  <Link to={`/empresas/list/empresa/${empresa.id_empresa}`}>
                    {empresa.nombre_empresa}
                  </Link>
                </Cell>
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {empresa.nif === null ? "-" : empresa.nif}
                  </div>
                </Cell>
                <Cell className="cellStyle">
                  <div style={{ whiteSpace: "normal" }}>
                    {empresa.pyme === null ? "-" : empresa.pyme ? "Sí" : "No"}
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

export default TableEmpresas;
