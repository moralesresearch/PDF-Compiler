// This is in your preload script
const { ipcRenderer } = require("electron");

ipcRenderer.on("updatePdfList", (event, pdfPath) => {
  const pdfList = document.getElementById("pdf-list");
  if (pdfList) {
    const listItem = document.createElement("li");
    listItem.textContent = pdfPath;
    pdfList.appendChild(listItem);
  }
});