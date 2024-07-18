import React from "react";

import { saveAs } from "file-saver";
import ExcelJS from "exceljs";
import Button from "react-bootstrap/Button";

const ExportarExcel = ({
  valoraciones,
  participaciones,
  empresas,
  filteredLicitaciones,
}) => {
  const handleExportToExcel = async () => {
    const workbook = new ExcelJS.Workbook();

    // Add worksheet for Licitaciones
    const licitacionesWorksheet = workbook.addWorksheet("Licitaciones");

    // Define headers for Licitaciones worksheet
    const licitacionesHeaders = [
      { header: "ID LICITACIÓN", key: "id_licitacion", width: 10 },
      { header: "EXPEDIENTE", key: "num_expediente", width: 50 },
      { header: "OBJETO", key: "objeto", width: 50 },
      { header: "PLAZO_PRESENTACION", key: "plazo_presentacion", width: 50 },
      { header: "DURACION", key: "plazo_ejecucion", width: 50 },
      { header: "PROCEDIMIENTO", key: "procedimiento", width: 50 },
      { header: "TRAMITACION", key: "tramitacion", width: 50 },
      {
        header: "IMPORTE (SIN IMPUESTOS)",
        key: "importe_sin_impuestos",
        width: 50,
      },
      {
        header: "IMPORTE (CON IMPUESTOS)",
        key: "importe_con_impuestos",
        width: 50,
      },
      {
        header: "VALOR ESTIMADO DEL CONTRATO",
        key: "valor_estimado",
        width: 50,
      },
      { header: "ADJUDICATARIO", key: "adjudicatario", width: 50 },
      { header: "LUGAR", key: "lugar_ejecucion", width: 50 },
      { header: "UNIDAD", key: "unidad_encargada", width: 50 },
      { header: "ABONOS A CUENTAS", key: "abonos_cuenta", width: 50 },
      { header: "TIPO DE CONTRATO", key: "tipo_contrato", width: 50 },
      {
        header: "CLASIFICACION SUBGRUPO",
        key: "clasificacion_subgrupo",
        width: 50,
      },
      { header: "CLASIFICACION GRUPO", key: "clasificacion_grupo", width: 50 },
      {
        header: "CLASIFICACION CATEGORÍA",
        key: "clasificacion_cat",
        width: 50,
      },
      {
        header: "CRITERIOS SOLVENCIA ECONÓMICA",
        key: "criterios_economica",
        width: 50,
      },
      {
        header: "MEDIOS SOLVENCIA ECONÓMICA",
        key: "medios_economica",
        width: 50,
      },
      {
        header: "CRITERIOS SOLVENCIA TÉCNICA",
        key: "criterios_tecnica",
        width: 50,
      },
      { header: "MEDIOS SOLVENCIA TÉCNICA", key: "medios_tecnica", width: 50 },
      {
        header: "CRITERIOS PARA DETECTAR VALORES ANORMALES",
        key: "criterios_valores_anormales",
        width: 50,
      },
      {
        header: "CONDICIOENS ESPECIALES",
        key: "condiciones_especiales",
        width: 50,
      },
      {
        header: "CONSIDERACIÓN COMO INFRACCIÓN GRAVE",
        key: "infraccion_grave",
        width: 50,
      },
      {
        header: "CONTRATACIÓN DEL CONTROL DE CALIDAD",
        key: "contratacion_control",
        width: 50,
      },
      { header: "FECHA ADJUDICACIÓN", key: "fecha_adjudicacion", width: 50 },
      { header: "FECHA FORMALIZACIÓN", key: "fecha_formalizacion", width: 50 },
      { header: "FECHA ANUNCIO", key: "fecha_anuncio", width: 50 },
      { header: "FORMA DE PAGO", key: "forma_pago", width: 50 },
      { header: "GARANTÍA DEFINITIVA", key: "garantia_def", width: 50 },
      { header: "GARANTÍA PROVISIONAL", key: "garantia_prov", width: 50 },
      {
        header: "GASTOS POR DESISTIMIENTO",
        key: "gastos_desistimiento",
        width: 50,
      },
      {
        header: "MODIFICACIONES PREVISTAS",
        key: "modificaciones_prev",
        width: 50,
      },
      { header: "PRÓRROGAS PREVISTAS", key: "prorrogas_prev", width: 50 },
      {
        header: "REVISIÓN DE PRECIOS PREVISTAS",
        key: "revision_precios_prev",
        width: 50,
      },
      {
        header: "ORTOS CONCEPTOS PREVISTOS",
        key: "otros_conceptos_prev",
        width: 50,
      },
      {
        header: "INCLUSIÓN DEL CONTROL DE CALIDAD",
        key: "inclusion_control_calidad",
        width: 50,
      },
      { header: "MEJORAS COMO CRITERIO", key: "mejora_criterio", width: 50 },
      {
        header: "OBLIGACIÓN DE INDICAR SUBCONTRATACIÓN",
        key: "obligacion_subcontratacion",
        width: 50,
      },
      {
        header: "OTROS COMPONENTES VALOR ESTIMADO",
        key: "otros_componentes",
        width: 50,
      },
      {
        header: "PENALIDADES POR INCUMPLIMIENTO",
        key: "penalidades_incumplimiento",
        width: 50,
      },
      { header: "PLAZO DE GARANTÍA", key: "plazo_garantia", width: 50 },
      { header: "PLAZO DE RECEPCIÓN", key: "plazo_recepcion", width: 50 },
      {
        header: "PLAZO MÁXIMO DE LAS PRÓRROGAS",
        key: "plazo_maximo_prorrogas",
        width: 50,
      },
      {
        header: "AMPLIACIÓN DE LA PRESENTACIÓN",
        key: "ampliacion_presentacion",
        width: 50,
      },
      {
        header: "POSIBILIDAD DE PRORROGAR EL CONTRATO",
        key: "posibilidad_prorroga",
        width: 50,
      },
      {
        header: "RÉGIMEN DE PENALIDADES",
        key: "regimen_penalidades",
        width: 50,
      },
      { header: "REVISIÓN DE PRECIOS", key: "revision_precios", width: 50 },
      { header: "SISTEMA DE PRECIOS", key: "sistema_precios", width: 50 },
      { header: "SUBASTA ELECTRÓNICA", key: "subasta_electronica", width: 50 },
      {
        header: "INDICAR SUBCONTRATACIÓN COMO CRITERIO",
        key: "subcontratacion_criterio",
        width: 50,
      },
      { header: "TAREAS CRÍTICAS", key: "tareas_criticas", width: 50 },
    ];

    // Set headers for Licitaciones worksheet
    licitacionesWorksheet.columns = licitacionesHeaders;

    // Populate data rows for Licitaciones worksheet
    filteredLicitaciones.forEach((licitacion) => {
      const row = {};
      licitacionesHeaders.forEach((header) => {
        row[header.key] = licitacion[header.key] || "";
      });
      licitacionesWorksheet.addRow(row);
    });

    // Step 1: Filter participaciones based on filteredLicitaciones
    const participacionesFiltradas = participaciones.filter((participacion) =>
      filteredLicitaciones.some(
        (licitacion) => licitacion.id_licitacion == participacion.id_licitacion
      )
    );

    // Step 2: Filter valoraciones based on participacionesFiltradas and add id_empresa
    const valoracionesFiltradas = valoraciones
      .map((valoracion) => {
        const participacion = participacionesFiltradas.find(
          (participacion) =>
            valoracion.id_participacion == participacion.id_participacion
        );
        if (participacion) {
          return {
            ...valoracion,
            id_empresa: participacion.id_empresa,
            id_licitacion: participacion.id_licitacion,
          };
        }
        return null;
      })
      .filter((valoracion) => valoracion.puntuacion !== null);

    // Step 3: Get unique criterio.nombre values from valoracionesFiltradas
    const uniquePairs = [
      ...new Set(
        valoracionesFiltradas.map(
          (valoracion) =>
            `${valoracion.id_criterio.nombre}_${valoracion.id_licitacion}`
        )
      ),
    ];
    const normalizeName = (name) => {
      return name.toUpperCase().replace(/[*/:?\\[\]]/g, ""); // Remove forbidden characters
    };
    const uniqueCriterios = [
      ...new Set(
        valoracionesFiltradas.map((valoracion) =>
          normalizeName(valoracion.id_criterio.nombre)
        )
      ),
    ];

    const summarySheet = workbook.addWorksheet("Summary");
    summarySheet.addRow(["Unique Criterios"]);
    uniqueCriterios.forEach((criterioNombre, index) => {
      summarySheet.addRow([`${index + 1}-${criterioNombre}`]);
    });

    const criterioWorksheets = {};
    uniqueCriterios.forEach((criterioNombre, index) => {
      const numberedCriterioNombre = `${index + 1}-${criterioNombre}`;
      const normalizedCriterioNombre = numberedCriterioNombre;
      const worksheet = workbook.addWorksheet(normalizedCriterioNombre);

      // Add headers for each licitacion
      const headers = ["EMPRESAS Y ESTADÍSTICAS"];
      filteredLicitaciones.forEach((licitacion) => {
        headers.push(`LICITACION (${licitacion.id_licitacion})`);
      });
      worksheet.addRow(headers);

      criterioWorksheets[criterioNombre] = worksheet;
    });
    const valoracionesMap = new Map();
    valoracionesFiltradas.forEach((valoracion) => {
      const key = `${normalizeName(valoracion.id_criterio.nombre)}_${
        valoracion.id_licitacion
      }_${valoracion.id_empresa}`;
      valoracionesMap.set(key, valoracion);
    });
    const valoracionesLicit = new Map();
    valoracionesFiltradas.forEach((valoracion) => {
      const key = `${normalizeName(valoracion.id_criterio.nombre)}_${
        valoracion.id_licitacion
      }`;
      valoracionesLicit.set(key, valoracion);
    });
    // Step 5: Populate valoraciones in each worksheet
    uniqueCriterios.forEach((criterioNombre) => {
      const worksheet = criterioWorksheets[criterioNombre];
      const rowPeso = ["PESO"];
      filteredLicitaciones.forEach((licitacion) => {
        var peso = "";
        const key = `${criterioNombre}_${licitacion.id_licitacion}`;
        const valoracion = valoracionesLicit.get(key);
        if (valoracion) {
          const criterio = valoracion.id_criterio;
          if (criterio) {
            peso = criterio.valor_max;
          }
        }
        rowPeso.push(peso);
      });
      worksheet.addRow(rowPeso);
      empresas.forEach((empresa) => {
        const row = [empresa.nombre_empresa];
        filteredLicitaciones.forEach((licitacion) => {
          const key = `${criterioNombre}_${licitacion.id_licitacion}_${empresa.id_empresa}`;
          const valoracion = valoracionesMap.get(key);

          if (valoracion) {
            row.push(valoracion.puntuacion);
          } else {
            row.push(""); // or any placeholder for missing values
          }
        });
        worksheet.addRow(row);
      });
    });
    // Generate Excel file and initiate download
    const buffer = await workbook.xlsx.writeBuffer();
    const blob = new Blob([buffer], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });
    saveAs(blob, "licitaciones.xlsx");
  };

  return (
    <>
      <Button variant="warning" onClick={handleExportToExcel}>
        Exportar a Excel
      </Button>
    </>
  );
};

export default ExportarExcel;
