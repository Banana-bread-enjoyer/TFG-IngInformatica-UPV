import React from "react";
import { saveAs } from "file-saver";
import ExcelJS from "exceljs";
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
    console.log(filters);

    const workbook = new ExcelJS.Workbook();

    if (filters || query) {
      const filtrosWorsheet = workbook.addWorksheet("Filtros");
      filtrosWorsheet.columns = [
        { header: "Filtro", key: "filter", width: 30 },
        { header: "Valor", key: "value", width: 50 },
      ];
      if (query && query != "") {
        filtrosWorsheet.addRow({
          filter: "Búsqueda",
          value: query || "N/A", // Use 'N/A' if the filter value is empty
        });
      }
      if (filters) {
        Object.entries(filters)
          .filter(([key, value]) => {
            // Handle lists separately
            if (Array.isArray(value)) {
              return value.length > 0; // Include if list is not empty
            }
            // Ensure value is treated as a string and check if it's not empty
            return value && String(value).trim() !== "";
          })
          .forEach(([key, value]) => {
            if (Array.isArray(value)) {
              // If value is a list, add each element in a new row
              value.forEach((item, index) => {
                filtrosWorsheet.addRow({
                  filter: `${names[key]} [${index + 1}]`, // Include index to differentiate items
                  value: `${item.num_cpv} - ${item.descripcion}` || "N/A", // Use 'N/A' if item is empty
                });
              });
            } else {
              // Convert value to string for consistency
              const strValue = String(value);
              const nameFilter = names[key];
              filtrosWorsheet.addRow({
                filter: nameFilter,
                value: strValue || "N/A", // Use 'N/A' if the filter value is empty
              });
            }
          });
      }
      filtrosWorsheet.getRow(1).font = { bold: true };
    }

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
      { header: "NIF", key: "nif", width: 50 },
      { header: "¿ES PYME?", key: "pyme", width: 50 },
      {
        header: "OFERTA ADJUDICATARIO",
        key: "oferta_adjudicatario",
        width: 50,
      },
      {
        header: "PUNTUACIÓN ECONÓMICA",
        key: "puntuacion_economica",
        width: 50,
      },
      { header: "PUNTUACIÓN TÉCNICA", key: "puntuacion_tecnica", width: 50 },
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
    const licitacionesData = filteredLicitaciones.map((licitacion) => {
      const row = {};
      licitacionesHeaders.forEach((header) => {
        var dato = licitacion[header.key];
        const participacionAdjudicatario = participaciones.find(
          (participacion) =>
            participacion.id_licitacion == licitacion.id_licitacion &&
            participacion.id_empresa == licitacion.adjudicatario.id_empresa
        );
        const puntuaciones = valoraciones.filter(
          (valoracion) =>
            valoracion.id_participacion ==
              participacionAdjudicatario.id_participacion &&
            valoracion.id_criterio.id_padre == null
        );

        if (header.key == "oferta_adjudicatario") {
          if (participacionAdjudicatario) {
            dato = participacionAdjudicatario.importe_ofertado_sin_iva;
          }
        } else if (header.key == "puntuacion_economica") {
          const puntEconomica = puntuaciones.find(
            (valoracion) =>
              valoracion.id_criterio.nombre.toUpperCase().includes("OFERTA") ||
              valoracion.id_criterio.nombre.toUpperCase().includes("PRECIO") ||
              valoracion.id_criterio.nombre.toUpperCase().includes("ECONÓMIC")
          );
          const puntFormulas = puntuaciones.find(
            (valoracion) =>
              valoracion.id_criterio.nombre.toUpperCase().includes("FÓRMULA") ||
              valoracion.id_criterio.nombre.toUpperCase().includes("FORMULA")
          );
          if (puntEconomica && puntFormulas) {
            dato = puntEconomica.puntuacion + puntFormulas.puntuacion;
          } else if (puntEconomica) {
            dato = puntEconomica.puntuacion;
          } else if (puntFormulas) {
            dato = puntFormulas.puntuacion;
          }
        } else if (header.key == "puntuacion_tecnica") {
          const puntTecnica = puntuaciones.find(
            (valoracion) =>
              valoracion.id_criterio.nombre.toUpperCase().includes("JUICIO") ||
              valoracion.id_criterio.nombre.toUpperCase().includes("MEMORIA")
          );
          if (puntTecnica) {
            dato = puntTecnica.puntuacion;
          }
        } else if (header.key == "adjudicatario") {
          dato = licitacion.adjudicatario.nombre_empresa;
        } else if (header.key == "tipo_contrato") {
          dato = licitacion.tipo_contrato.nombre_tipo_contrato;
        } else if (header.key == "procedimiento") {
          dato = licitacion.procedimiento.nombre_procedimiento;
        } else if (header.key == "tramitacion") {
          dato = licitacion.tramitacion.nombre_tramitacion;
        } else if (header.key == "nif") {
          dato = licitacion.adjudicatario.nif;
        } else if (header.key == "pyme") {
          dato = licitacion.adjudicatario.pyme;
        }
        if (typeof dato == "boolean") {
          dato = dato ? "Sí" : "No";
        }
        const numberPattern = /^-?\d+(\.\d+)?$/;
        if (
          typeof dato == "string" &&
          numberPattern.test(dato) &&
          !header.key.includes("prev")
        ) {
          dato = Number(dato);
        }
        row[header.key] = dato || "";
      });
      return row;
    });
    licitacionesWorksheet.addRows(licitacionesData);

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
      .filter((valoracion) => valoracion && valoracion.puntuacion !== null);

    // Step 3: Get unique criterio.nombre values from valoracionesFiltradas
    const uniqueCriterios = [
      ...new Set(
        valoracionesFiltradas.map((valoracion) =>
          valoracion.id_criterio.nombre
            .toUpperCase()
            .replace(/[*/:?\\[\]]/g, "")
        )
      ),
    ];
    //Hoja de Empresas
    const empresasSheet = workbook.addWorksheet("Listado de Empresas");
    const headersEmpresas = [
      "EMPRESAS",
      "PARTICIPACIONES",
      "ADJUDICACIONES",
      "PORCENTAJE DE ÉXITO",
    ];
    empresasSheet.addRow(headersEmpresas);
    empresas.forEach((empresa) => {
      const participacionesEmpresa = participacionesFiltradas.filter(
        (participacion) => participacion.id_empresa == empresa.id_empresa
      ).length;
      const adjudicacionesEmpresa = filteredLicitaciones.filter(
        (licitacion) =>
          licitacion.adjudicatario.id_empresa == empresa.id_empresa
      ).length;
      const exito =
        participacionesEmpresa != 0
          ? (adjudicacionesEmpresa / participacionesEmpresa) * 100
          : 0;
      const row = [
        empresa.nombre_empresa,
        participacionesEmpresa,
        adjudicacionesEmpresa,
        exito,
      ];
      empresasSheet.addRow(row);
      const columnWidths = [70, 20, 20, 20]; // Width for 'EMPRESAS Y ESTADÍSTICAS'
      empresasSheet.columns = columnWidths.map((width) => ({ width }));
    });
    //Hoja de criterios
    const summarySheet = workbook.addWorksheet("Listado de Criterios");
    summarySheet.columns = [
      { header: "Criterios", key: "criterio", width: 200 }, // Adjust width as needed
    ];
    uniqueCriterios.forEach((criterioNombre, index) => {
      summarySheet.addRow([`${index + 1}-${criterioNombre}`]);
    });

    const participacionesMap = new Map();
    participacionesFiltradas.forEach((participacion) => {
      const key = `${participacion.id_licitacion}_${participacion.id_empresa}`;
      participacionesMap.set(key, participacion);
    });

    //Hoja oferta economica
    const ofertaWorksheet = workbook.addWorksheet("OFERTA ECONÓMICA");
    const headers = ["EMPRESAS Y PRESUPUESTO"];
    filteredLicitaciones.forEach((licitacion) => {
      headers.push(`LICITACION (${licitacion.id_licitacion})`);
    });
    ofertaWorksheet.addRow(headers);
    const columnWidths = [70]; // Width for 'EMPRESAS Y ESTADÍSTICAS'
    filteredLicitaciones.forEach(() => {
      columnWidths.push(20); // Width for each 'LICITACION' column
    });
    ofertaWorksheet.columns = columnWidths.map((width) => ({ width }));
    const rowPresupuesto = ["PRESUPUESTO BASE DE LICITACIÓN SIN IVA"];
    filteredLicitaciones.forEach((licitacion) => {
      rowPresupuesto.push(
        licitacion.importe_sin_impuestos
          ? Number(licitacion.importe_sin_impuestos)
          : licitacion.importe_sin_impuestos
      );
    });
    ofertaWorksheet.addRow(rowPresupuesto);
    empresas.forEach((empresa) => {
      const row = [empresa.nombre_empresa];
      filteredLicitaciones.forEach((licitacion) => {
        const key = `${licitacion.id_licitacion}_${empresa.id_empresa}`;
        const participacion = participacionesMap.get(key);
        row.push(
          participacion
            ? participacion.importe_ofertado_sin_iva
              ? Number(participacion.importe_ofertado_sin_iva)
              : ""
            : ""
        );
      });
      ofertaWorksheet.addRow(row);
    });
    //Hoja individual para cada criterio
    const criterioWorksheets = {};
    uniqueCriterios.forEach((criterioNombre, index) => {
      const numberedCriterioNombre = `${index + 1}-${criterioNombre}`;
      const worksheet = workbook.addWorksheet(numberedCriterioNombre);

      // Add headers for each licitacion
      const headers = ["EMPRESAS Y ESTADÍSTICAS"];
      filteredLicitaciones.forEach((licitacion) => {
        headers.push(`LICITACION (${licitacion.id_licitacion})`);
      });
      worksheet.addRow(headers);
      const columnWidths = [70]; // Width for 'EMPRESAS Y ESTADÍSTICAS'
      filteredLicitaciones.forEach(() => {
        columnWidths.push(20); // Width for each 'LICITACION' column
      });
      worksheet.columns = columnWidths.map((width) => ({ width }));
      criterioWorksheets[criterioNombre] = worksheet;
    });

    const valoracionesMap = new Map();
    valoracionesFiltradas.forEach((valoracion) => {
      const key = `${valoracion.id_criterio.nombre
        .toUpperCase()
        .replace(/[*/:?\\[\]]/g, "")}_${valoracion.id_licitacion}_${
        valoracion.id_empresa
      }`;
      valoracionesMap.set(key, valoracion);
    });

    // Step 5: Populate valoraciones in each worksheet
    uniqueCriterios.forEach((criterioNombre) => {
      const worksheet = criterioWorksheets[criterioNombre];

      const rowPeso = ["PESO"];
      filteredLicitaciones.forEach((licitacion) => {
        const key = `${criterioNombre}_${licitacion.id_licitacion}`;
        const valoracion = valoracionesFiltradas.find(
          (val) =>
            `${val.id_criterio.nombre
              .toUpperCase()
              .replace(/[*/:?\\[\]]/g, "")}_${val.id_licitacion}` === key
        );
        rowPeso.push(valoracion ? valoracion.id_criterio.valor_max : "");
      });
      worksheet.addRow(rowPeso);

      empresas.forEach((empresa) => {
        const row = [empresa.nombre_empresa];
        filteredLicitaciones.forEach((licitacion) => {
          const key = `${criterioNombre}_${licitacion.id_licitacion}_${empresa.id_empresa}`;
          const valoracion = valoracionesMap.get(key);
          row.push(valoracion ? valoracion.puntuacion : "");
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
        <CalculateIcon className="me-2" />
        Exportar a Excel
      </Button>
    </>
  );
};

export default ExportarExcel;
