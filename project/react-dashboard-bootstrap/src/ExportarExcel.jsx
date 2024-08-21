import React from "react";
import { saveAs } from "file-saver";
import Button from "react-bootstrap/Button";
import CalculateIcon from "@mui/icons-material/Calculate";

const ExportarExcel = ({
  valoraciones,
  participaciones,
  empresas,
  filteredLicitaciones,
  filters,
  query,
}) => {
  const names = {
    lugarEjecucion: "Lugar de Ejecución",
    importeMax: "Importe Máximo",
    importeMin: "Importe Mínimo",
    unidadEncargada: "Unidad Encargada",
    plazoPresentacionDesde: "Plazo de Presentación (Desde)",
    plazoPresentacionHasta: "Plazo de Presentación (Hasta)",
    tipoContrato: "Tipo de Contrato",
    tipoProcedimiento: "Tipo de Procedimiento",
    tipoTramitacion: "Tipo de Tramitación",
    codigoCPV: "Código CPV",
  };
  const handleExportToExcel = async () => {
    // Configurar los parámetros de la consulta
    const params = new URLSearchParams({
      query: query || "",
      filtros: JSON.stringify(filters) || "{}",
    });

    try {
      // Realizar la solicitud al backend para obtener el archivo Excel
      const response = await fetch(
        `http://localhost:8000/api/exportar_excel/?${params.toString()}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Error en la solicitud de exportación");
      }

      // Convertir la respuesta en un blob y guardar el archivo
      const blob = await response.blob();
      saveAs(blob, "licitaciones.xlsx");
    } catch (error) {
      console.error("Error al exportar a Excel:", error);
    }
  };

  return (
    <Button variant="warning" onClick={handleExportToExcel}>
      <CalculateIcon className="me-2" />
      Exportar a Excel
    </Button>
  );
};

export default ExportarExcel;
