import sys
import os
import PyPDF2
from PyPDF2 import PdfFileMerger
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QLabel, QLineEdit, \
    QFileDialog, QMessageBox, QAction, QMenuBar, QDialog, QVBoxLayout as VBoxLayout

# Global list to store PDF file paths
pdf_files = []


class PDFCompiler(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Compiler")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # List to display PDF file names
        self.pdf_list_widget = QListWidget(self)

        # Output file name input
        self.output_label = QLabel("Output File Name:", self)
        self.output_edit = QLineEdit(self)

        self.init_ui()

    def init_ui(self):
        # Layouts
        layout = QVBoxLayout(self.central_widget)

        # Add widgets to layouts
        layout.addWidget(self.pdf_list_widget)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_edit)

        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")

        # Add actions to the File menu
        add_action = QAction("Add PDF", self)
        remove_action = QAction("Remove PDF", self)
        clear_action = QAction("Clear List", self)
        combine_action = QAction("Combine PDFs", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(add_action)
        file_menu.addAction(remove_action)
        file_menu.addAction(clear_action)
        file_menu.addAction(combine_action)
        file_menu.addAction(exit_action)

        # Add action to the Help menu for "About"
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Connect actions to functions
        add_action.triggered.connect(self.add_pdf)
        remove_action.triggered.connect(self.remove_pdf)
        clear_action.triggered.connect(self.clear_list)
        combine_action.triggered.connect(self.combine_pdfs)
        exit_action.triggered.connect(self.close)

        # Connect "About" action to display the about dialog
        about_action.triggered.connect(self.show_about_dialog)

    def add_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog(self, options=options)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        file_paths, _ = file_dialog.getOpenFileNames()

        if file_paths:
            pdf_files.extend(file_paths)
            self.update_list()

    def remove_pdf(self):
        selected_item = self.pdf_list_widget.currentItem()

        if selected_item:
            pdf_files.pop(self.pdf_list_widget.row(selected_item))
            self.pdf_list_widget.takeItem(self.pdf_list_widget.row(selected_item))

    def clear_list(self):
        pdf_files.clear()
        self.pdf_list_widget.clear()

    def combine_pdfs(self):
        if not pdf_files:
            QMessageBox.warning(self, "Warning", "No PDFs selected.")
            return

        output_file, _ = QFileDialog.getSaveFileName(self, "Save As", "", "PDF Files (*.pdf)")

        if output_file:
            pdf_merger = PdfFileMerger()

            for pdf_file in pdf_files:
                pdf_merger.append(pdf_file)

            pdf_merger.write(output_file)
            pdf_merger.close()

            QMessageBox.information(self, "Success", "PDFs combined successfully.")
            self.clear_list()
            self.output_edit.clear()
            self.update_list()

    def update_list(self):
        self.pdf_list_widget.clear()
        self.pdf_list_widget.addItems([os.path.basename(pdf_file) for pdf_file in pdf_files])

    def show_about_dialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About PDF Compiler")
        about_dialog.setGeometry(200, 200, 400, 200)
        layout = VBoxLayout(about_dialog)

        version_label = QLabel("Version: 3.0", about_dialog)
        name_label = QLabel("Name: PDF Compiler", about_dialog)
        copyright_label = QLabel("Copyright © 2023 Morales Research Inc and Erick Suarez", about_dialog)
        release_label = QLabel("Released on September 3, 2023", about_dialog)

        layout.addWidget(name_label)
        layout.addWidget(version_label)
        layout.addWidget(copyright_label)
        layout.addWidget(release_label)

        about_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFCompiler()
    window.show()
    sys.exit(app.exec_())
