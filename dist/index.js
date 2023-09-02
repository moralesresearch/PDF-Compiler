"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
const path = require("path");
const fs = require("fs/promises");
const pdf_lib_1 = require("pdf-lib");
let mainWindow = null;
const pdfFiles = [];
electron_1.app.whenReady().then(() => {
    mainWindow = new electron_1.BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, "src/preload.js"), // Load the preload script
        },
    });
    mainWindow.loadFile("src/index.html");
    electron_1.app.on("activate", function () {
        if (electron_1.BrowserWindow.getAllWindows().length === 0)
            createWindow();
    });
    electron_1.ipcMain.on("addPdfToList", (event, pdfPath) => {
        mainWindow === null || mainWindow === void 0 ? void 0 : mainWindow.webContents.send("updatePdfList", pdfPath);
    });
});
electron_1.app.on("window-all-closed", function () {
    if (process.platform !== "darwin")
        electron_1.app.quit();
});
const menuTemplate = [
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
const menu = electron_1.Menu.buildFromTemplate(menuTemplate);
electron_1.Menu.setApplicationMenu(menu);
function openPdfFile() {
    return __awaiter(this, void 0, void 0, function* () {
        const file = electron_1.dialog.showOpenDialogSync({
            filters: [
                { name: "PDF Files", extensions: ["pdf"] },
                { name: "All Files", extensions: ["*"] },
            ],
            properties: ["openFile"],
        });
        if (file) {
            const pdfPath = file[0];
            try {
                const pdfDoc = yield pdf_lib_1.PDFDocument.load(yield fs.readFile(pdfPath));
                // Do something with the loaded PDF document (e.g., add it to a list)
                pdfFiles.push({ path: pdfPath, document: pdfDoc });
                // Update your user interface to show the loaded PDFs
                // (e.g., update a list or display thumbnails)
                const pdfList = document.getElementById("pdf-list");
                if (pdfList) {
                    const listItem = document.createElement("li");
                    listItem.textContent = path.basename(pdfPath); // Display only the filename
                    pdfList.appendChild(listItem);
                }
                else {
                    console.error("Element with id 'pdf-list' not found in the DOM.");
                }
            }
            catch (error) {
                console.error("Error loading PDF:", error);
            }
        }
    });
}
function mergePdfs() {
    return __awaiter(this, void 0, void 0, function* () {
        if (pdfFiles.length < 2) {
            electron_1.dialog.showMessageBoxSync({ type: "info", title: "Merge PDFs", message: "Select at least two PDFs to merge." });
            return;
        }
        const mergedPdf = yield pdf_lib_1.PDFDocument.create();
        for (const { document } of pdfFiles) {
            const copiedPages = yield mergedPdf.copyPages(document, document.getPageIndices());
            copiedPages.forEach((page) => mergedPdf.addPage(page));
        }
        const savePath = electron_1.dialog.showSaveDialogSync({
            filters: [{ name: "PDF Files", extensions: ["pdf"] }],
        });
        if (savePath) {
            try {
                const mergedPdfBytes = yield mergedPdf.save();
                fs.writeFile(savePath, mergedPdfBytes);
                electron_1.dialog.showMessageBoxSync({ type: "info", title: "Merge PDFs", message: `PDFs merged and saved to ${savePath}` });
            }
            catch (error) {
                console.error("Error saving merged PDF:", error);
            }
        }
    });
}
function showAbout() {
    const aboutMessage = "PDF Compiler\nVersion 3.0\nCopyright © 2023 Morales Research Inc";
    electron_1.dialog.showMessageBoxSync({ type: "info", title: "About", message: aboutMessage });
}
electron_1.app.on("ready", createWindow);
electron_1.app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        electron_1.app.quit();
    }
});
electron_1.app.on("activate", () => {
    if (mainWindow === null) {
        createWindow();
    }
});
function createWindow() {
    throw new Error("Function not implemented.");
}
