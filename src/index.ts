import { app, BrowserWindow, Menu, ipcMain, MenuItemConstructorOptions, dialog } from "electron";
import * as path from "path";
import * as fs from "fs/promises";
import { PDFDocument } from "pdf-lib";

let mainWindow: BrowserWindow | null = null;
const pdfFiles: { path: string; document: PDFDocument }[] = [];

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false, // Disable nodeIntegration in the main process
      contextIsolation: true, // Enable context isolation
      preload: path.join(__dirname, "src/preload.js"), // Load the preload script
    },
  });

  mainWindow.loadFile("src/index.html");

  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });

  ipcMain.on("addPdfToList", (event, pdfPath) => {
    mainWindow?.webContents.send("updatePdfList", pdfPath);
  });
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

  const menuTemplate: MenuItemConstructorOptions[] = [
    {
      label: "File",
      submenu: [
        {
          label: "Open PDF",
          click: openPdfFile,
        },
        {
          label: "Merge PDFs",
          click: mergePdfs,
        },
        {
          label: "Exit",
          role: "quit",
        },
      ],
    },
    {
      label: "Help",
      submenu: [
        {
          label: "About",
          click: showAbout,
        },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(menuTemplate);
  Menu.setApplicationMenu(menu);


async function openPdfFile() {
  const file = dialog.showOpenDialogSync({
    filters: [
      { name: "PDF Files", extensions: ["pdf"] },
      { name: "All Files", extensions: ["*"] },
    ],
    properties: ["openFile"],
  });

  if (file) {
    const pdfPath = file[0];
    try {
      const pdfDoc = await PDFDocument.load(await fs.readFile(pdfPath));
      // Do something with the loaded PDF document (e.g., add it to a list)
      pdfFiles.push({ path: pdfPath, document: pdfDoc });
      // Update your user interface to show the loaded PDFs
      // (e.g., update a list or display thumbnails)
      const pdfList = document.getElementById("pdf-list");
      if (pdfList) {
        const listItem = document.createElement("li");
        listItem.textContent = path.basename(pdfPath); // Display only the filename
        pdfList.appendChild(listItem);
      } else {
        console.error("Element with id 'pdf-list' not found in the DOM.");
      }
    } catch (error) {
      console.error("Error loading PDF:", error);
    }
  }
}

async function mergePdfs() {
  if (pdfFiles.length < 2) {
    dialog.showMessageBoxSync({ type: "info", title: "Merge PDFs", message: "Select at least two PDFs to merge." });
    return;
  }

  const mergedPdf = await PDFDocument.create();

  for (const { document } of pdfFiles) {
    const copiedPages = await mergedPdf.copyPages(document, document.getPageIndices());
    copiedPages.forEach((page) => mergedPdf.addPage(page));
  }

  const savePath = dialog.showSaveDialogSync({
    filters: [{ name: "PDF Files", extensions: ["pdf"] }],
  });

  if (savePath) {
    try {
      const mergedPdfBytes = await mergedPdf.save();
      fs.writeFile(savePath, mergedPdfBytes);
      dialog.showMessageBoxSync({ type: "info", title: "Merge PDFs", message: `PDFs merged and saved to ${savePath}` });
    } catch (error) {
      console.error("Error saving merged PDF:", error);
    }
  }
}

function showAbout() {
  const aboutMessage = "PDF Compiler\nVersion 3.0\nCopyright © 2023 Morales Research Inc";
  dialog.showMessageBoxSync({ type: "info", title: "About", message: aboutMessage });
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

function createWindow() {
  throw new Error("Function not implemented.");
}
