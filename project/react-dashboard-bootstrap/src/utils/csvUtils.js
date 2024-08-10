function convertArrayToCSV(data) {
  const headers = data[0];
  const rows = data.slice(1);

  const csvContent = [
    headers.join(","), // headers row first
    ...rows.map((row) => row.join(",")),
  ].join("\n");

  return csvContent;
}

function downloadCSV(csvContent, fileName = "data.csv") {
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", fileName);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
