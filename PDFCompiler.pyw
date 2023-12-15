import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt
import PyPDF3

os.environ['QT_MAC_WANTS_LAYER'] = '1'

class DraggableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if file_path.endswith('.pdf'):
                    self.addItem(os.path.basename(file_path))
                    self.window().pdf_paths[os.path.basename(file_path)] = file_path

class PDFCompiler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_paths = {}
        self.initUI()

    def initUI(self):
        # Create a central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Set the window title
        self.setWindowTitle("PDF Compiler")

        # Create and add widgets to the layout
        self.pdf_list = DraggableListWidget(self)
        add_button = QPushButton('Add PDFs', self)
        combine_button = QPushButton('Combine PDFs', self)
        self.result_label = QLabel('', self)

        # Add widgets to the layout
        layout.addWidget(self.pdf_list)
        layout.addWidget(add_button)
        layout.addWidget(combine_button)
        layout.addWidget(self.result_label)

        # Connect the button click events
        add_button.clicked.connect(self.add_pdfs)
        combine_button.clicked.connect(self.combine_pdfs)

        # Create About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)

        # Add About action to the application menu on macOS
        if sys.platform == "darwin":
            menu_bar = self.menuBar()
            app_menu = menu_bar.addMenu('&App')
            app_menu.addAction(about_action)

    def add_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDFs", "", "PDF Files (*.pdf)")
        for file in files:
            if file.endswith('.pdf'):
                self.pdf_list.addItem(os.path.basename(file))
                self.pdf_paths[os.path.basename(file)] = file

    def combine_pdfs(self):
        pdf_files = [self.pdf_paths[self.pdf_list.item(i).text()] for i in range(self.pdf_list.count())]
        if not pdf_files:
            self.result_label.setText("No PDF files to combine.")
            return

        # Create a PDF writer object
        pdf_writer = PyPDF3.PdfFileWriter()

        # Loop through each PDF file and add its pages to the writer
        for pdf_path in pdf_files:
            pdf_reader = PyPDF3.PdfFileReader(pdf_path)
            for page in range(pdf_reader.numPages):
                pdf_writer.add_page(pdf_reader.getPage(page))

        # Save the combined PDF
        output_filename, _ = QFileDialog.getSaveFileName(self, "Save Combined PDF", "", "PDF Files (*.pdf)")
        if output_filename:
            with open(output_filename, 'wb') as out_pdf:
                pdf_writer.write(out_pdf)
            self.result_label.setText(f"Combined PDF saved as {os.path.basename(output_filename)}")
        else:
            self.result_label.setText("PDF combining cancelled.")

    def show_about_dialog(self):
        QMessageBox.about(self, "About PDF Compiler", "PDF Compiler\nVersion 1.0\nCopyright 2023")

if __name__ == '__main__':
    app = QApplication([])
    ex = PDFCompiler()
    ex.show()
    app.exec()

